package parser

// PASS: simple balanced – New + Wrap in same function
func f_top(db *DepthBox) {
    db.New()
    db.Wrap()
}
