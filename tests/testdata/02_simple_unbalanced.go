package parser

// FAIL: only New, no Wrap
func f_top(db *DepthBox) {
    db.New()
}
