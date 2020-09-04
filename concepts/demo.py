from extractor import TextRank4Keyword

text = "North Carolina kicked off the process Friday, sending hundreds of thousands of mail-in ballots to voters. Other states are set to follow throughout the month as election officials brace for historic levels of voting by mail as the coronavirus pandemic continues to grip the country. That shift is playing out against the backdrop of consistent and unfounded attacks from President Donald Trump, who this week encouraged people in North Carolina to test the system by voting twice -- once by mail and once in person, which election officials said would be illegal.Despite Trump's efforts to paint mail-in voting as prone to fraud, it's as secure or more secure than traditional methods of voting, according to the National Conference of State Legislatures. (More on that in a minute). But the shift away from in-person voting will accelerate the election timeline. Almost every US state has a mail-in ballot application deadline in October. So what does this mean for Election Day? As CNN's Joan Biskupic reports: Some Democratic lawyers have begun arguing that states could take until late December to submit their Electoral College totals. Some Republican lawyers counter that earlier dates are hard and fast. Election law experts, meanwhile, note that Congress could change the archaic law at any point and establish new deadlines. The bottom line: The one date fixed by the US Constitution is January 20, at noon, when the four-year term of the president and vice president ends and the next begins."

tr4w = TextRank4Keyword()
tr4w.analyze(text, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
tr4w.get_keywords(10)