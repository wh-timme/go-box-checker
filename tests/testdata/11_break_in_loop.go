package parser

// PASS: break after Wrap inside loop
func f_top(db *DepthBox) {
    for i := 0; i < n; i++ {
        db.New()
        db.Wrap()
        if done {
            break
        }
    }
}
