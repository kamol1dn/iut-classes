/*
 * ball.c - BALL.  Tap to flip gravity; roll on the floor or the ceiling.   PURE C.
 *
 * A ball rolls right along a corridor that scrolls past it.  Gravity pulls it
 * to the floor - until A is tapped while it is touching a surface: then
 * gravity FLIPS and the ball falls up to the ceiling and rolls along that.
 * Tapping in the air does nothing (a tap up to 4 ticks before landing is
 * remembered, so a slightly early tap still counts).
 *
 * The corridor comes in SECTIONS.  Each section has hazards on ONE side -
 * spikes, blocks, blocks with spikes on top - and the ball must be rolling on
 * the OTHER side to get through.  Between two sections whose hazards are on
 * different sides there is a plain stretch of corridor: the moment to flip.
 *
 * The physics is FLAP's two lines, with a sign that can change:
 *
 *     vy += dir * GRAVITY;        dir = +1 falls down, -1 falls up
 *     y  += vy;
 *
 * and a landing rule: if the ball would sink into the surface it is falling
 * towards, it is put back on top of it and stops - "grounded", the only state
 * in which a tap flips.  Hitting the SIDE of a block, or touching a spike,
 * ends the game.  Score = distance rolled, one point per 8 px.
 *
 * ball_sim() is one tick of all that, on a state struct and nothing else, so
 * the host test's autopilot can try futures without touching the game.
 */
#include "engine.h"

#define BALL_X     24                   /* the ball's screen column (centre)  */
#define R          3                    /* radius: the ball is 7 x 7          */
#define RING       256                  /* corridor columns kept               */
#define RMASK      (RING - 1)
#define BASE_FL    59                   /* floor surface: rows 59..63 solid   */
#define BASE_CE    13                   /* ceiling: rows FIELD_Y..13 solid    */
#define GRAVITY    40                   /* 1/256 px per tick^2                */
#define KICK       64                   /* speed away from the surface on a flip */
#define VMAX       768                  /* 3 px per tick                       */
#define BUF_TICKS  4                    /* an early tap is remembered this long */
#define RUNUP      120                  /* plain corridor before the first hazard */
#define AHEAD      64                   /* columns generated past the screen   */
#define WAIT_AUTO  (3 * TICK_HZ)
#define PX_PER_PT  8

static int8_t  fl[RING], ce[RING];      /* floor surface row, ceiling last row */
static int8_t  sf[RING], sc[RING];      /* spike height on the floor / ceiling */

/* the generator */
static int32_t gen_x, start_x;
static int     hz;                      /* hazards on: 0 the floor, 1 the ceiling */
static int     sec_left, trans_left, feat_kind, feat_w, feat_left, feat_h, first_feat;

static ball_state_t st;
static int     level, speed, waiting, wait_ticks, stick_zone, milestone;
static int32_t score;

static int shown_cam = -1, shown_y = -1, shown_prompt, need_full;

/* ---- the corridor ---------------------------------------------------------- */
enum { F_GAP, F_SPIKES, F_BLOCK, F_BLOCK_SPIKES };
static const int8_t spike_shape[6] = { 1, 3, 6, 6, 3, 1 };

static int window(void) { return 24 - 2 * level; }   /* the flip stretch: 22 .. 14 px */

static void new_feature(void)
{
    int k = (int)rng_below(first_feat ? 3 : 4) + (first_feat ? 1 : 0);
    first_feat = 0;
    feat_h = 0;
    switch (k) {
    case F_GAP:          feat_w = 4 + (int)rng_below(8);                         break;
    case F_SPIKES:       feat_w = 6 * (1 + (int)rng_below(3));                   break;
    case F_BLOCK:        feat_w = 8 + (int)rng_below(17); feat_h = 4 + (int)rng_below(13); break;
    default:             feat_w = 6 * (1 + (int)rng_below(2)); feat_h = 4 + (int)rng_below(7); break;
    }
    if (feat_w > sec_left + 1) { k = F_GAP; feat_w = sec_left + 1; feat_h = 0; }
    feat_kind = k;  feat_left = feat_w;
}

/* One more column on the right of the corridor. */
static void gen_column(void)
{
    int32_t c = gen_x++;
    int f = BASE_FL, e = BASE_CE, s = 0, block = 0;
    if (c - start_x >= RUNUP) {
        while (trans_left == 0 && sec_left == 0) {          /* a new section  */
            int nhz = rng_below(100) < 65 ? !hz : hz;
            trans_left = (nhz != hz) ? window() : 6;
            hz = nhz;
            sec_left = 48 + (int)rng_below(65);
            feat_left = 0;  first_feat = 1;
        }
        if (trans_left > 0) {
            trans_left--;                                   /* plain: flip here */
        } else {
            sec_left--;
            if (feat_left == 0) { new_feature(); }
            int pos = feat_w - feat_left;
            feat_left--;
            block = feat_h;
            if (feat_kind == F_SPIKES || feat_kind == F_BLOCK_SPIKES) { s = spike_shape[pos % 6]; }
        }
    }
    if (hz == 0) { f -= block; } else { e += block; }
    fl[c & RMASK] = (int8_t)f;  ce[c & RMASK] = (int8_t)e;
    sf[c & RMASK] = (int8_t)(hz == 0 ? s : 0);
    sc[c & RMASK] = (int8_t)(hz == 1 ? s : 0);
}

static int solid(int32_t c, int r) { return r >= fl[c & RMASK] || r <= ce[c & RMASK]; }

/* ---- one tick of physics: the whole game, minus score and sound ------------- */
int ball_sim(ball_state_t *s, int pace, int press, int *flipped)
{
    *flipped = 0;
    if (press) { s->buf = BUF_TICKS; }
    if (s->buf > 0) {
        if (s->grounded) {                                  /* flip!          */
            s->dir = -s->dir;  s->vy = s->dir * KICK;
            s->grounded = 0;  s->buf = 0;  *flipped = 1;
        } else {
            s->buf--;
        }
    }

    /* forward: the columns the ball's front edge enters this tick.  Any rock
     * in rows y-2..y+2 there is the side of a block - fatal.  (Rows y+-3, the
     * ball's top and bottom, are spared, so a 1-px bump is rolled over.) */
    int y = (int)(s->y >> FP);
    int32_t f0 = (s->cam >> FP) + BALL_X + R;
    s->cam += pace;
    int32_t f1 = (s->cam >> FP) + BALL_X + R;
    for (int32_t c = f0 + 1; c <= f1; c++) {
        for (int r = y - 2; r <= y + 2; r++) { if (solid(c, r)) { return 1; } }
    }

    /* up or down: Euler, then land on whatever is under (or over) the ball */
    s->vy += s->dir * GRAVITY;
    if (s->vy > VMAX)  { s->vy = VMAX; }
    if (s->vy < -VMAX) { s->vy = -VMAX; }
    s->y += s->vy;
    y = (int)(s->y >> FP);
    int32_t x = (s->cam >> FP) + BALL_X;
    s->grounded = 0;
    if (s->dir > 0) {
        int top = OLED_H;
        for (int32_t c = x - 2; c <= x + 2; c++) { if (fl[c & RMASK] < top) { top = fl[c & RMASK]; } }
        if (y + R >= top) { y = top - R - 1; s->y = (int32_t)y << FP; s->vy = 0; s->grounded = 1; }
    } else {
        int bot = 0;
        for (int32_t c = x - 2; c <= x + 2; c++) { if (ce[c & RMASK] > bot) { bot = ce[c & RMASK]; } }
        if (y - R <= bot) { y = bot + R + 1; s->y = (int32_t)y << FP; s->vy = 0; s->grounded = 1; }
    }

    /* spikes: a triangle's hitbox is its upper part, 2 px short of the base
     * ... and of the tip, so a graze the player cannot see does not count */
    for (int32_t c = x - 2; c <= x + 2; c++) {
        int h = sf[c & RMASK], g = fl[c & RMASK];
        if (h > 2 && y + 2 >= g - h + 2 && y - 2 <= g - 1) { return 1; }
        h = sc[c & RMASK];  g = ce[c & RMASK];
        if (h > 2 && y - 2 <= g + h - 2 && y + 2 >= g + 1) { return 1; }
    }
    return 0;
}

static int pace_now(void) { int up = 8 * (int)(score / 50); return speed + (up > 64 ? 64 : up); }

/* ---- the game --------------------------------------------------------------- */
static void ball_start(int lvl)
{
    level = lvl;  score = 0;  milestone = 0;
    speed = 192 + 32 * (lvl - 1);       /* 0.75 .. 1.25 px per tick           */
    start_x = 0;  gen_x = 0;  hz = 1;
    sec_left = 0;  trans_left = 0;  feat_left = 0;
    st.cam = 0;  st.y = (int32_t)(BASE_FL - R - 1) << FP;  st.vy = 0;
    st.dir = 1;  st.grounded = 1;  st.buf = 0;
    waiting = 1;  wait_ticks = 0;  stick_zone = 0;
    while (gen_x <= OLED_W + AHEAD) { gen_column(); }
    need_full = 1;  shown_cam = -1;
}

static int ball_step(const pad_t *in)
{
    /* A tap is an EDGE: A going down, or the stick pushed up or down. */
    int zone = in->y > 50 ? 1 : in->y < -50 ? -1 : 0;
    int press = (in->pressed & PAD_A) || (zone != 0 && stick_zone == 0);
    stick_zone = zone;

    if (waiting) {                      /* the tap that starts is not a flip  */
        if (press || ++wait_ticks >= WAIT_AUTO) { waiting = 0; }
        return 0;
    }

    int pace = pace_now();
    while (gen_x <= ((st.cam + pace) >> FP) + OLED_W + AHEAD) { gen_column(); }
    int flipped;
    if (ball_sim(&st, pace, press, &flipped)) { sfx(SFX_LOSE); return 1; }
    if (flipped) { sfx(SFX_BOUNCE); }

    int32_t s = ((st.cam >> FP) - start_x) / PX_PER_PT;
    if (s > score) {
        score = s;
        if (score / 100 > milestone) { milestone = (int)(score / 100); sfx(SFX_LEVEL); }
        else if (score % 25 == 0)    { sfx(SFX_POINT); }
    }
    return 0;
}

/* ---- drawing ---------------------------------------------------------------- */
static void ball_draw(int full)
{
    int cx = (int)(st.cam >> FP), y = (int)(st.y >> FP);
    if (!full && !need_full && cx == shown_cam && y == shown_y && shown_prompt == waiting) {
        return;                                              /* nothing moved */
    }
    if (full || need_full) { oled_clear(); need_full = 0; }
    else { oled_fill_rect(0, FIELD_Y, OLED_W, OLED_H - FIELD_Y, OLED_OFF); }

    for (int x = 0; x < OLED_W; x++) {
        int32_t c = cx + x;
        int f = fl[c & RMASK], e = ce[c & RMASK];
        int pf = fl[(c - 1) & RMASK], pe = ce[(c - 1) & RMASK];
        oled_vline(x, f, 2, OLED_ON);                        /* surfaces, 2 px */
        oled_vline(x, e - 1, 2, OLED_ON);
        if (x > 0 && f != pf) {                              /* block sides    */
            oled_vline(x, f < pf ? f : pf, (f < pf ? pf - f : f - pf) + 1, OLED_ON);
        }
        if (x > 0 && e != pe) {
            oled_vline(x, e < pe ? e : pe, (e < pe ? pe - e : e - pe) + 1, OLED_ON);
        }
        for (int r = FIELD_Y; r < OLED_H; r += 2) {          /* the rock: dots */
            if (r > e - 3 && r < f + 3) { continue; }
            if (((c + ((r >> 1) & 1) * 2) & 3) == 0) { oled_pixel(x, r, OLED_ON); }
        }
        if (sf[c & RMASK]) { oled_vline(x, f - sf[c & RMASK], sf[c & RMASK], OLED_ON); }
        if (sc[c & RMASK]) { oled_vline(x, e + 1, sc[c & RMASK], OLED_ON); }
    }

    /* the ball, with a spoke that turns as it rolls - the other way round
     * when it rolls along the ceiling */
    static const int8_t spoke[4][2] = { {3, 0}, {2, 2}, {0, 3}, {-2, 2} };
    int a = (cx / 3) & 3;
    if (st.dir < 0) { a = (4 - a) & 3; }
    oled_fill_circle(BALL_X, y, R, OLED_OFF);
    oled_circle(BALL_X, y, R, OLED_ON);
    oled_line(BALL_X - spoke[a][0], y - spoke[a][1], BALL_X + spoke[a][0], y + spoke[a][1], OLED_ON);

    if (waiting) {
        oled_fill_rect(40, 31, 49, 9, OLED_OFF);
        oled_text(43, 32, "A: FLIP", OLED_ON);
    }
    shown_cam = cx;  shown_y = y;  shown_prompt = waiting;
    hud("BALL", score, -1, full);
}

static int32_t ball_score(void) { return score; }

const game_t game_ball = { "BALL", ball_start, ball_step, ball_draw, ball_score };

/* ---- for the host test ---------------------------------------------------- */
void ball_get(ball_state_t *s, int *pace) { *s = st;  *pace = pace_now(); }

void ball_peek(peek_t *p)
{
    p->x = BALL_X;  p->y = (int)(st.y >> FP);  p->w = 2 * R + 1;  p->h = 2 * R + 1;
    p->tx = (int)(st.cam >> FP);  p->ty = hz;
    p->vx = speed;  p->vy = (int)st.vy;
    p->gap = st.dir;  p->count = (int)score;  p->lives = waiting;
}
