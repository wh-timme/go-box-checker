package parser

// PASS: nested loop body has balanced New + Wrap
func f_top(db *DepthBox) {
	LABEL:
	for {
		db.New()
		switch mode {
			case 1:
				db.New()
			case 2:
				db.New()
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
			case 3:
				for {
					db.New()
					switch mode {
						case 1:
							db.New()
						default:
							db.Wrap()
							db.Wrap()
							continue LABEL
					}
					db.Wrap()
					db.Wrap()
					db.Wrap()
					break LABEL
				}
			default:
				db.Wrap()
				continue
		}
		db.Wrap()
		db.Wrap()
		break
	}
}
