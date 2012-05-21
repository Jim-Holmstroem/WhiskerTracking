for f in $(ls -1 *.png)
do
	convert $f -crop 280x250+258+0 $f
done

