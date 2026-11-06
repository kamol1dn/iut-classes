/*
 * wave.c - WAVE.  Hold to climb, let go to dive, both at 45 degrees.   PURE C.
 *
 * A dart flies right through a cave that scrolls past it.  It never moves
 * straight: while A (or the stick up) is HELD it climbs at 45 degrees, and
 * the moment it is released it dives at 45 degrees.  So the whole game is
 * one bit of input per tick, and the dart's path is a zig-zag - drawn behind
 * it as a trail.
 *
 * 45 degrees means the vertical speed IS the horizontal speed:
 *
 *     cam += speed;                       the cave scrolls left by speed
 *     y   += held ? -speed : +speed;      the dart climbs or dives as much
 *
 * Both in fixed point (1/256 px), so a speed of 1.25 px per tick is exact.
 *
 * The cave is a ring buffer of columns, one per world pixel: top[c] is the
 * last row of the ceiling, bot[c] the first row of the floor.  New columns
 * are generated ahead of the screen in SEGMENTS: for 8..39 columns the
 * ceiling and floor each slope by -1, 0 or +1 px per column - flat or 45
 * degrees, the same angles the dart flies, so a skilled player can skim a
 * slope.  The gap is never allowed below `gmin`, which shrinks as the score
 * rises, so the cave is always passable and always getting tighter.
 *
 * Touching the ceiling or the floor ends the game.  Score = distance flown,
 * one point per 8 px.
 */
#include "engine.h"

#define WAVE_X     24                   /* the dart's screen column           */
#define RING       256                  /* cave columns kept: > 128 + WAVE_X  */
#define RMASK      (RING - 1)
#define TOP_MIN    (FIELD_Y + 1)        /* the ceiling is at least 2 rows     */
#define BOT_MAX    (OLED_H - 2)         /* the floor is at least 2 rows       */
#define GAP_MAX    40
#define FLAT_START 96                   /* a straight run-up before the cave  */
#define WAIT_AUTO  (3 * TICK_HZ)        /* starts by itself after 3 s         */
#define PX_PER_PT  8                    /* score: one point per 8 px          */

static int8_t  top[RING], bot[RING];    /* the cave, by world column & RMASK  */
static int8_t  trail[RING];             /* the dart's y at each world column  */
static int32_t gen_x;                   /* next world column to generate      */
static int     seg_left, ts, bs;        /* the current segment: slopes, length */

static int32_t cam;                     /* world x of screen column 0, 1/256 px */
static int32_t wy;                      /* the dart's y, 1/256 px             */
static int32_t start_x;                 /* world column where the trail begins */
static int     level, speed, gmin0, waiting, wait_ticks, going_up, milestone;
static int32_t score;

static int shown_cam = -1, shown_y = -1, shown_up = -1, shown_prompt, need_full;

/* ---- the cave ------------------------------------------------------------- */
static int gmin_now(void)
{
    int g = gmin0 - (int)(score / 40);   /* one pixel tighter every 40 points  */
    return g < 12 ? 12 : g;
}

static void new_segment(void)
{
    seg_left = 8 + (int)rng_below(32);
    ts = (int)rng_below(3) - 1;         /* -1 up, 0 flat, +1 down             */
    bs = (int)rng_below(3) - 1;
}

/* One more column on the right of the cave. */
static void gen_column(void)
{
    int32_t c = gen_x;
    int t = top[(c - 1) & RMASK], b = bot[(c - 1) & RMASK];
    if (c - start_x < FLAT_START) {                         /* the run-up     */
        top[c & RMASK] = (int8_t)t;  bot[c & RMASK] = (int8_t)b;
        gen_x++;
        return;
    }
    if (--seg_left <= 0) { new_segment(); }
    int g = gmin_now();
    int nt = t + ts, nb = b + bs;
    if (nt < TOP_MIN) { nt = TOP_MIN; ts = 0; }
    if (nb > BOT_MAX) { nb = BOT_MAX; bs = 0; }
    if (nb - nt < g) {                  /* too tight: undo the narrowing      */
        if (nt > t) { nt = t; ts = 0; }
        if (nb < b) { nb = b; bs = 0; }
        if (nb - nt < g) { nb = nt + g; if (nb > BOT_MAX) { nb = BOT_MAX; nt = nb - g; } }
    }
    if (nb - nt > GAP_MAX) {            /* too wide: undo the widening        */
        if (nt < t) { nt = t; ts = 0; }
        if (nb > b) { nb = b; bs = 0; }
    }
    top[c & RMASK] = (int8_t)nt;  bot[c & RMASK] = (int8_t)nb;
    gen_x++;
}

/* The dart's hitbox is 3 x 3 around its centre - small, like the real
 * thing: a hit the player can see is fair.  1 if it touches rock. */
int wave_hits(int32_t wx, int y)
{
    for (int32_t c = wx - 1; c <= wx + 1; c++) {
        if (y - 1 <= top[c & RMASK] || y + 1 >= bot[c & RMASK]) { return 1; }
    }
    return 0;
}

/* a little faster every 50 points, at most 1/4 px per tick faster */
static int pace_now(void) { int up = 8 * (int)(score / 50); return speed + (up > 64 ? 64 : up); }

/* ---- the game --------------------------------------------------------------- */
static void wave_start(int lvl)
{
    level = lvl;  score = 0;  milestone = 0;
    speed = 192 + 32 * (lvl - 1);       /* 0.75 .. 1.25 px per tick           */
    gmin0 = 30 - 3 * lvl;               /* 27 px at level 1 .. 15 at level 5  */
    cam = 0;  start_x = 0;
    int mid = (FIELD_Y + OLED_H) / 2;
    wy = (int32_t)mid << FP;
    waiting = 1;  wait_ticks = 0;  going_up = 0;
    /* a wide straight tunnel to start in */
    top[RMASK] = (int8_t)(mid - 16);  bot[RMASK] = (int8_t)(mid + 16);
    gen_x = 0;
    new_segment();
    for (int i = 0; i < RING; i++) { trail[i] = (int8_t)mid; }
    while (gen_x < OLED_W + 1) { gen_column(); }
    need_full = 1;  shown_cam = -1;
}

static int wave_step(const pad_t *in)
{
    /* HELD, not pressed: the wave climbs for as long as the button is down. */
    int held = (in->down & PAD_A) || in->y > 50;

    if (waiting) {
        if (held || ++wait_ticks >= WAIT_AUTO) { waiting = 0; }
        else { return 0; }
    }
    going_up = held;

    int pace = pace_now();
    int32_t x0 = (cam >> FP) + WAVE_X, y0 = wy >> FP;
    cam += pace;
    wy  += held ? -pace : pace;
    int32_t x1 = (cam >> FP) + WAVE_X, y1 = wy >> FP;

    while (gen_x <= (cam >> FP) + OLED_W) { gen_column(); }

    /* the trail: every column crossed this tick, its y on the straight line */
    for (int32_t c = x0 + 1; c <= x1; c++) {
        int y = (int)(y0 + (y1 - y0) * (c - x0) / (x1 - x0));
        trail[c & RMASK] = (int8_t)y;
    }

    int32_t s = ((cam >> FP) + WAVE_X - start_x) / PX_PER_PT;
    if (s > score) {
        score = s;
        if (score / 100 > milestone) { milestone = (int)(score / 100); sfx(SFX_LEVEL); }
        else if (score % 25 == 0)    { sfx(SFX_POINT); }
    }

    return wave_hits(x1, (int)y1);
}

/* ---- drawing ---------------------------------------------------------------- */
static void dart(int x, int y, int up, int colour)
{
    /* a little arrowhead pointing along the 45-degree path */
    int d = up ? -1 : 1;
    oled_line(x - 2, y - 2 * d, x + 2, y + 2 * d, colour);   /* the shaft      */
    oled_line(x + 2, y + 2 * d, x - 1, y + 2 * d, colour);   /* the head ...   */
    oled_line(x + 2, y + 2 * d, x + 2, y - d, colour);       /* ... both sides */
}

static void wave_draw(int full)
{
    int cx = (int)(cam >> FP), y = (int)(wy >> FP);
    if (!full && !need_full && cx == shown_cam && y == shown_y && going_up == shown_up
        && shown_prompt == waiting) {
        return;                                              /* nothing moved */
    }
    if (full || need_full) { oled_clear(); need_full = 0; }
    else { oled_fill_rect(0, FIELD_Y, OLED_W, OLED_H - FIELD_Y, OLED_OFF); }

    for (int x = 0; x < OLED_W; x++) {
        int32_t c = cx + x;
        int t = top[c & RMASK], b = bot[c & RMASK];
        oled_vline(x, t - 1, 2, OLED_ON);                    /* the edges, 2 px */
        oled_vline(x, b, 2, OLED_ON);
        /* the rock: staggered dots, fixed to the world so they scroll with it
         * - dots, not lines, so they never look like the dart's trail */
        for (int r = FIELD_Y; r < OLED_H; r += 2) {
            if (r > t - 3 && r < b + 3) { continue; }
            if (((c + ((r >> 1) & 1) * 2) & 3) == 0) { oled_pixel(x, r, OLED_ON); }
        }
        if (x < WAVE_X && c > start_x) {                     /* the zig-zag    */
            oled_pixel(x, trail[c & RMASK], OLED_ON);
        }
    }
    dart(WAVE_X, y, going_up, OLED_ON);
    if (waiting) {
        oled_fill_rect(37, 49, 55, 9, OLED_OFF);
        oled_text(40, 50, "HOLD A", OLED_ON);
    }
    shown_cam = cx;  shown_y = y;  shown_up = going_up;  shown_prompt = waiting;
    hud("WAVE", score, -1, full);
}

static int32_t wave_score(void) { return score; }

const game_t game_wave = { "WAVE", wave_start, wave_step, wave_draw, wave_score };

/* ---- for the host test ---------------------------------------------------- */
void wave_peek(peek_t *p)
{
    /* tx/ty: the middle of the cave a few columns ahead of the dart */
    int32_t c = (cam >> FP) + WAVE_X + 6;
    p->x = WAVE_X;  p->y = (int)(wy >> FP);  p->w = 3;  p->h = 3;
    p->tx = (int)c;
    p->ty = (top[c & RMASK] + bot[c & RMASK]) / 2;
    p->gap = bot[c & RMASK] - top[c & RMASK];
    p->vx = speed;  p->vy = going_up ? -speed : speed;
    p->count = (int)score;  p->lives = waiting;
}

/* The exact state, so the host test's autopilot can look ahead with the
 * game's own arithmetic and wave_hits(). */
void wave_state(int32_t *cam_fp, int32_t *y_fp, int *pace)
{
    *cam_fp = cam;  *y_fp = wy;  *pace = pace_now();
}
