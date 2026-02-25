package parser

// PASS: recursive call with delta=0
func f_top(db *DepthBox) {
    db.New()
    f_expr(db)
    db.Wrap()
}

func f_expr(db *DepthBox) {
    db.New()
    f_expr(db)
    db.Wrap()
}
