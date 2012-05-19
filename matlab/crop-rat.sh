for file in $(ls -1 rat-*.png); do
	convert $file -crop 500x300+215+200 $cropopts $file
done

