package parser

// FAIL: if branch has Wrap, else does not
func f_top(db *DepthBox) {
    db.New()
    if cond {
        db.Wrap()
    } else {
        // missing Wrap
    }
}
