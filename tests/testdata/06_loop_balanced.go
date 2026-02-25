package parser

// PASS: loop body has balanced New + Wrap
func f_top(db *DepthBox) {
    for i := 0; i < n; i++ {
        db.New()
        db.Wrap()
    }
}
