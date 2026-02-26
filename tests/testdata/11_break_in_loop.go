package parser

// PASS: break without Wrap inside loop
func f_top(db *DepthBox) {
    for {
        db.New()
		if mode {
            db.Wrap()
		} else {
			break
		}
    }
	db.Wrap()
}
