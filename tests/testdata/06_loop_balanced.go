package parser

// PASS: loop body has balanced New + Wrap
func f_top(db *DepthBox) {
    for i := 0; i < n; i++ {
        db.New()
        db.Wrap()
    }
	for f_cond() {}
	for {
		db.New()
		switch mode {
			case 1:
				db.New()
			default:
				db.Wrap()
				continue
		}
		db.Wrap()
		db.Wrap()
		break
	}
}

func f_cond(db *DepthBox) bool {
	db.New()
	db.Wrap()
	return false
}
