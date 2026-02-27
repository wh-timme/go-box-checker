package parser

// Stress cat-07: fallthrough chains

func f_s07_bal_000(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_001(db *DepthBox) {
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
}

func f_s07_bal_002(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_003(db *DepthBox) {
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
}

func f_s07_bal_004(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_005(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_006(db *DepthBox) {
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
}

func f_s07_bal_007(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_008(db *DepthBox) {
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
}

func f_s07_bal_009(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_010(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_011(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_012(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_013(db *DepthBox) {
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
}

func f_s07_bal_014(db *DepthBox) {
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
}

func f_s07_bal_015(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_bal_016(db *DepthBox) {
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
}

func f_s07_bal_017(db *DepthBox) {
	db.New()
	switch mode {
	case 1:
		fallthrough
	case 2:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
}

func f_s07_unb_018(db *DepthBox) {
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		fallthrough
	case 2:
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
}

func f_s07_unb_019(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		fallthrough
	case 2:
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_unb_020(db *DepthBox) {
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
}

func f_s07_unb_021(db *DepthBox) {
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.New()
		fallthrough
	case 2:
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
}

func f_s07_unb_022(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_unb_023(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_unb_024(db *DepthBox) {
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
}

func f_s07_unb_025(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_unb_026(db *DepthBox) {
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
}

func f_s07_unb_027(db *DepthBox) {
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		fallthrough
	case 2:
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
}

func f_s07_unb_028(db *DepthBox) {
	db.New()
	switch mode {
	case 1:
		db.New()
		fallthrough
	case 2:
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
}

func f_s07_unb_029(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		fallthrough
	case 2:
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_unb_030(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		fallthrough
	case 2:
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_unb_031(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		fallthrough
	case 2:
		db.Wrap()
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_unb_032(db *DepthBox) {
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.New()
		fallthrough
	case 2:
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
}

func f_s07_unb_033(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		fallthrough
	case 2:
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_unb_034(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		fallthrough
	case 2:
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

func f_s07_unb_035(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	switch mode {
	case 1:
		db.New()
		fallthrough
	case 2:
		db.Wrap()
	default:
		panic("discard")
}
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
db.Wrap()
}

