package parser

// Stress cat-08: panic path pruning

func f_s08_bal_000(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if active {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_001(db *DepthBox) {
	db.New()
	if ok {
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_002(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	if done {
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_003(db *DepthBox) {
	db.New()
	if done {
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_004(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	if mode_ok {
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_005(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if found {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_006(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	if mode_ok {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_007(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	if active {
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_008(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if valid {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_009(db *DepthBox) {
	db.New()
	if ok {
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_010(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if mode_ok {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_011(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if ready {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_012(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	if active {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_013(db *DepthBox) {
	db.New()
	db.New()
	if valid {
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_014(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	if active {
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_015(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	if valid {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_016(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if ok {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_bal_017(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	if valid {
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_018(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	if flag {
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_019(db *DepthBox) {
	db.New()
	db.New()
	if active {
	} else {
		panic("discard")
	}
}

func f_s08_unb_020(db *DepthBox) {
	db.New()
	if ok {
	} else {
		panic("discard")
	}
}

func f_s08_unb_021(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	if ok {
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_022(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if done {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_023(db *DepthBox) {
	db.New()
	if mode_ok {
	} else {
		panic("discard")
	}
}

func f_s08_unb_024(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if ok {
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_025(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	if valid {
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_026(db *DepthBox) {
	db.New()
	if flag {
	} else {
		panic("discard")
	}
}

func f_s08_unb_027(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	if ok {
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_028(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if ready {
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_029(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if active {
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_030(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if ok {
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_031(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if mode_ok {
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_032(db *DepthBox) {
	db.New()
	if flag {
	} else {
		panic("discard")
	}
}

func f_s08_unb_033(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if valid {
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
		db.Wrap()
	} else {
		panic("discard")
	}
}

func f_s08_unb_034(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if mode_ok {
	} else {
		panic("discard")
	}
}

func f_s08_unb_035(db *DepthBox) {
	db.New()
	db.New()
	db.New()
	db.New()
	db.New()
	if flag {
	} else {
		panic("discard")
	}
}

