package parser

// PASS: nested loop body has balanced New + Wrap
func f_top(db *DepthBox) {
	LABEL_FOR:
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
						case 2:
							db.New()
							break
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
					LABEL_SW:
					switch mode {
						case 1:
							db.New()
						case 2:
							db.New()
							break LABEL_SW
						default:
							db.Wrap()
							db.Wrap()
							continue LABEL_FOR
					}
					db.Wrap()
					db.Wrap()
					db.Wrap()
					break LABEL_FOR
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
