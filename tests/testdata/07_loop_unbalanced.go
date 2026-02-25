package parser

// FAIL: loop body only has New
func f_top(db *DepthBox) {
    for i := 0; i < n; i++ {
        db.New()
    }
}
