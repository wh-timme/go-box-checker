package parser

// PASS: panic paths discarded
func f_top(db *DepthBox) {
    db.New()
	if inside_if_else {
        if cond {
            db.Wrap()
        } else {
            panic("discard")
        }
	} else {
    	switch mode {
    	case 1:
            db.Wrap()
    	case 2:
            fallthrough
    	default:
            panic("discard")
    	}
	}
}
