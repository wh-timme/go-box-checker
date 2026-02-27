package parser

// Stress cat-05: for with condition function call

func f_s05_cond_000(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_bal_000(db *DepthBox) {
	for f_s05_cond_000() {
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	}
}

func f_s05_cond_001(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_bal_001(db *DepthBox) {
	for f_s05_cond_001() {
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	}
}

func f_s05_cond_002(db *DepthBox) bool {
	return false
}

func f_s05_bal_002(db *DepthBox) {
	for f_s05_cond_002() {
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	}
}

func f_s05_cond_003(db *DepthBox) bool {
	return false
}

func f_s05_bal_003(db *DepthBox) {
	for f_s05_cond_003() {
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
	}
}

func f_s05_cond_004(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_bal_004(db *DepthBox) {
	for f_s05_cond_004() {
	}
}

func f_s05_cond_005(db *DepthBox) bool {
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_bal_005(db *DepthBox) {
	for f_s05_cond_005() {
		db.New()
		db.Wrap()
	}
}

func f_s05_cond_006(db *DepthBox) bool {
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
	return false
}

func f_s05_bal_006(db *DepthBox) {
	for f_s05_cond_006() {
	}
}

func f_s05_cond_007(db *DepthBox) bool {
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
	return false
}

func f_s05_bal_007(db *DepthBox) {
	for f_s05_cond_007() {
	}
}

func f_s05_cond_008(db *DepthBox) bool {
	return false
}

func f_s05_bal_008(db *DepthBox) {
	for f_s05_cond_008() {
		db.New()
		db.Wrap()
	}
}

func f_s05_cond_009(db *DepthBox) bool {
	db.New()
	db.Wrap()
	return false
}

func f_s05_bal_009(db *DepthBox) {
	for f_s05_cond_009() {
	}
}

func f_s05_cond_010(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_bal_010(db *DepthBox) {
	for f_s05_cond_010() {
		db.New()
		db.Wrap()
	}
}

func f_s05_cond_011(db *DepthBox) bool {
	db.New()
	db.Wrap()
	return false
}

func f_s05_bal_011(db *DepthBox) {
	for f_s05_cond_011() {
		db.New()
		db.Wrap()
	}
}

func f_s05_cond_012(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_bal_012(db *DepthBox) {
	for f_s05_cond_012() {
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
	}
}

func f_s05_cond_013(db *DepthBox) bool {
	return false
}

func f_s05_bal_013(db *DepthBox) {
	for f_s05_cond_013() {
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	}
}

func f_s05_cond_014(db *DepthBox) bool {
	db.New()
	db.Wrap()
	return false
}

func f_s05_bal_014(db *DepthBox) {
	for f_s05_cond_014() {
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	}
}

func f_s05_cond_015(db *DepthBox) bool {
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
	return false
}

func f_s05_bal_015(db *DepthBox) {
	for f_s05_cond_015() {
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	}
}

func f_s05_cond_016(db *DepthBox) bool {
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_bal_016(db *DepthBox) {
	for f_s05_cond_016() {
		db.New()
		db.Wrap()
	}
}

func f_s05_cond_017(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_bal_017(db *DepthBox) {
	for f_s05_cond_017() {
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	}
}

func f_s05_cond_018(db *DepthBox) bool {
	db.New()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_018(db *DepthBox) {
	for f_s05_cond_018() {
	}
}

func f_s05_cond_019(db *DepthBox) bool {
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_019(db *DepthBox) {
	for f_s05_cond_019() {
	}
}

func f_s05_cond_020(db *DepthBox) bool {
	db.New()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_020(db *DepthBox) {
	for f_s05_cond_020() {
	}
}

func f_s05_cond_021(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_021(db *DepthBox) {
	for f_s05_cond_021() {
	}
}

func f_s05_cond_022(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_022(db *DepthBox) {
	for f_s05_cond_022() {
	}
}

func f_s05_cond_023(db *DepthBox) bool {
	db.New()
	db.New()
	return false
}

func f_s05_unb_023(db *DepthBox) {
	for f_s05_cond_023() {
	}
}

func f_s05_cond_024(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.Wrap()
	return false
}

func f_s05_unb_024(db *DepthBox) {
	for f_s05_cond_024() {
	}
}

func f_s05_cond_025(db *DepthBox) bool {
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_025(db *DepthBox) {
	for f_s05_cond_025() {
	}
}

func f_s05_cond_026(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_026(db *DepthBox) {
	for f_s05_cond_026() {
	}
}

func f_s05_cond_027(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	return false
}

func f_s05_unb_027(db *DepthBox) {
	for f_s05_cond_027() {
	}
}

func f_s05_cond_028(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	return false
}

func f_s05_unb_028(db *DepthBox) {
	for f_s05_cond_028() {
	}
}

func f_s05_cond_029(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_029(db *DepthBox) {
	for f_s05_cond_029() {
	}
}

func f_s05_cond_030(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_030(db *DepthBox) {
	for f_s05_cond_030() {
	}
}

func f_s05_cond_031(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	return false
}

func f_s05_unb_031(db *DepthBox) {
	for f_s05_cond_031() {
	}
}

func f_s05_cond_032(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_032(db *DepthBox) {
	for f_s05_cond_032() {
	}
}

func f_s05_cond_033(db *DepthBox) bool {
	db.New()
	db.Wrap()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_033(db *DepthBox) {
	for f_s05_cond_033() {
	}
}

func f_s05_cond_034(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	return false
}

func f_s05_unb_034(db *DepthBox) {
	for f_s05_cond_034() {
	}
}

func f_s05_cond_035(db *DepthBox) bool {
	db.New()
	db.New()
	db.New()
	db.New()
	db.Wrap()
	db.Wrap()
	return false
}

func f_s05_unb_035(db *DepthBox) {
	for f_s05_cond_035() {
	}
}

