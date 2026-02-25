package parser

// PASS: cross-function – f_open does New, f_close does Wrap
func f_top(db *DepthBox) {
    f_open(db)
    f_close(db)
}

func f_open(db *DepthBox) {
    db.New()
}

func f_close(db *DepthBox) {
    db.Wrap()
}
