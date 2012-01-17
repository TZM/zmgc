all: phoenix-quartz.png phoenix-cairo.png phoenix.png phoenix.pdf version


%.pdf: %.dot
	dot -Kneato -T -n pdf $< -o  $@

%.png: %.dot
	dot -Kneato -T -n png $< -o  $@

%-quartz.png: %.dot
	dot -Kneato -T -n png:quartz $< -o $(addsuffix -quartz.png, $(basename $< .dot) )

%-cairo.png: %.dot
	dot -Kneato -T -n png:cairo $< -o $(addsuffix -cairo.png, $(basename $< .dot) )

version:
	dot -V
	uname -a
    
clean:
	@- rm phoenix-cairo.png phoenix-quartz.png phoenix.pdf phoenix.png