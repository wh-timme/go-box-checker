package parser

// PASS: all switch cases balanced
func f_top(db *DepthBox) {
    db.New()
    switch x {
    case 1:
        db.Wrap()
    case 2:
        db.Wrap()
    default:
        db.Wrap()
    }
}
