package parser

// PASS: all switch cases balanced
func f_top(db *DepthBox) {
    db.New()
    switch x {
    case 1:
        db.Wrap()
    case 2:
		fallthrough
    case 3:
        db.Wrap()
        db.New()
        db.Wrap()
    default:
        panic("discard")
    }
}
