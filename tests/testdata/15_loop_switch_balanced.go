package parser

// PASS: loop + switch body has balanced New + Wrap
func f_top(db *DepthBox) {
	db.New()
	LABEL:
	for {
		switch mode {
			case 1:
				db.New()
			case 2:
				continue
			case 3:
				fallthrough
			default:
				db.Wrap()
				break LABEL
		}
		db.Wrap()
		db.Wrap()
		break
	}
}
