package parser

// FAIL: loop condition only has New
func f_top(db *DepthBox) {
	for f_cond() {}
}

func f_cond(db *DepthBox) bool {
	db.New()
	return false
}
