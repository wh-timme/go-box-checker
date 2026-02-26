package parser

// PASS: recursive call with delta=0
func f_top(db *DepthBox) {
    db.New()
    f_expr(db)
}

func f_expr(db *DepthBox) {
	switch mode {
		case 1:
			db.New()
			f_expr(db)
		default: ;
	}
    db.Wrap()
}
