package parser

// Stress cat-14: recursive and mutual recursive

func f_s14_bal_000(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_000(db)
		db.Wrap()
}
}

func f_s14_bal_001(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_001(db)
		db.Wrap()
}
}

func f_s14_bal_002(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_002(db)
		db.Wrap()
}
}

func f_s14_bal_003(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_003(db)
		db.Wrap()
}
}

func f_s14_bal_004(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_004(db)
		db.Wrap()
}
}

func f_s14_bal_005(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_005(db)
		db.Wrap()
}
}

func f_s14_bal_006(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_006(db)
		db.Wrap()
}
}

func f_s14_bal_007(db *DepthBox) {
	switch mode {
	case 1:
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
		db.New()
		f_s14_bal_007(db)
		db.Wrap()
}
}

func f_s14_bal_008(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_008(db)
		db.Wrap()
}
}

func f_s14_bal_009(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_009(db)
		db.Wrap()
}
}

func f_s14_bal_010(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_010(db)
		db.Wrap()
}
}

func f_s14_bal_011(db *DepthBox) {
	switch mode {
	case 1:
	default:
		db.New()
		f_s14_bal_011(db)
		db.Wrap()
}
}

func f_s14_bal_012(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_012(db)
		db.Wrap()
}
}

func f_s14_bal_013(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_013(db)
		db.Wrap()
}
}

func f_s14_bal_014(db *DepthBox) {
	switch mode {
	case 1:
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
		db.New()
		f_s14_bal_014(db)
		db.Wrap()
}
}

func f_s14_bal_015(db *DepthBox) {
	switch mode {
	case 1:
	default:
		db.New()
		f_s14_bal_015(db)
		db.Wrap()
}
}

func f_s14_bal_016(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_016(db)
		db.Wrap()
}
}

func f_s14_bal_017(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_bal_017(db)
		db.Wrap()
}
}

func f_s14_unb_018(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_018(db)
		db.Wrap()
}
}

func f_s14_unb_019(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.New()
	default:
		db.New()
		f_s14_unb_019(db)
		db.Wrap()
}
}

func f_s14_unb_020(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_020(db)
		db.Wrap()
}
}

func f_s14_unb_021(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_021(db)
		db.Wrap()
}
}

func f_s14_unb_022(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_022(db)
		db.Wrap()
}
}

func f_s14_unb_023(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.New()
	default:
		db.New()
		f_s14_unb_023(db)
		db.Wrap()
}
}

func f_s14_unb_024(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_024(db)
		db.Wrap()
}
}

func f_s14_unb_025(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_025(db)
		db.Wrap()
}
}

func f_s14_unb_026(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_026(db)
		db.Wrap()
}
}

func f_s14_unb_027(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_027(db)
		db.Wrap()
}
}

func f_s14_unb_028(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.New()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_028(db)
		db.Wrap()
}
}

func f_s14_unb_029(db *DepthBox) {
	switch mode {
	case 1:
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_029(db)
		db.Wrap()
}
}

func f_s14_unb_030(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.New()
		db.New()
	default:
		db.New()
		f_s14_unb_030(db)
		db.Wrap()
}
}

func f_s14_unb_031(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_unb_031(db)
		db.Wrap()
}
}

func f_s14_unb_032(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_032(db)
		db.Wrap()
}
}

func f_s14_unb_033(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_033(db)
		db.Wrap()
}
}

func f_s14_unb_034(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.New()
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_034(db)
		db.Wrap()
}
}

func f_s14_unb_035(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	default:
		db.New()
		f_s14_unb_035(db)
		db.Wrap()
}
}

func f_s14_mbal_a_036(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_b_036(db)
		db.Wrap()
}
}

func f_s14_mbal_b_036(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_a_036(db)
		db.Wrap()
}
}

func f_s14_mbal_a_037(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_b_037(db)
		db.Wrap()
}
}

func f_s14_mbal_b_037(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_a_037(db)
		db.Wrap()
}
}

func f_s14_mbal_a_038(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_b_038(db)
		db.Wrap()
}
}

func f_s14_mbal_b_038(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_a_038(db)
		db.Wrap()
}
}

func f_s14_mbal_a_039(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_b_039(db)
		db.Wrap()
}
}

func f_s14_mbal_b_039(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_a_039(db)
		db.Wrap()
}
}

func f_s14_mbal_a_040(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_b_040(db)
		db.Wrap()
}
}

func f_s14_mbal_b_040(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_a_040(db)
		db.Wrap()
}
}

func f_s14_mbal_a_041(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_b_041(db)
		db.Wrap()
}
}

func f_s14_mbal_b_041(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_a_041(db)
		db.Wrap()
}
}

func f_s14_mbal_a_042(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_b_042(db)
		db.Wrap()
}
}

func f_s14_mbal_b_042(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_a_042(db)
		db.Wrap()
}
}

func f_s14_mbal_a_043(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_b_043(db)
		db.Wrap()
}
}

func f_s14_mbal_b_043(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_a_043(db)
		db.Wrap()
}
}

func f_s14_mbal_a_044(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_b_044(db)
		db.Wrap()
}
}

func f_s14_mbal_b_044(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		db.New()
		f_s14_mbal_a_044(db)
		db.Wrap()
}
}

func f_s14_munb_a_045(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_munb_b_045(db)
}
}

func f_s14_munb_b_045(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		f_s14_munb_a_045(db)
}
}

func f_s14_munb_a_046(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_munb_b_046(db)
}
}

func f_s14_munb_b_046(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		f_s14_munb_a_046(db)
}
}

func f_s14_munb_a_047(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_munb_b_047(db)
}
}

func f_s14_munb_b_047(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		f_s14_munb_a_047(db)
}
}

func f_s14_munb_a_048(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_munb_b_048(db)
}
}

func f_s14_munb_b_048(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		f_s14_munb_a_048(db)
}
}

func f_s14_munb_a_049(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_munb_b_049(db)
}
}

func f_s14_munb_b_049(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		f_s14_munb_a_049(db)
}
}

func f_s14_munb_a_050(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_munb_b_050(db)
}
}

func f_s14_munb_b_050(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		f_s14_munb_a_050(db)
}
}

func f_s14_munb_a_051(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_munb_b_051(db)
}
}

func f_s14_munb_b_051(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		f_s14_munb_a_051(db)
}
}

func f_s14_munb_a_052(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_munb_b_052(db)
}
}

func f_s14_munb_b_052(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		f_s14_munb_a_052(db)
}
}

func f_s14_munb_a_053(db *DepthBox) {
	switch mode {
	case 1:
		db.New()
	default:
		db.New()
		f_s14_munb_b_053(db)
}
}

func f_s14_munb_b_053(db *DepthBox) {
	switch mode {
	case 1:
		; // base
	default:
		f_s14_munb_a_053(db)
}
}

