package placeholder

type Replacer struct {
	Placeholder string `mapstructure:"placeholder"`
	Replacement string `mapstructure:"replacement"`
	IsURLPath   bool   `mapstructure:"IsURLPath"`
}
