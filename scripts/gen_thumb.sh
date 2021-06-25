#!/bin/bash
for file in "$@"
do
  # next line checks the mime-type of the file
  IMAGE_TYPE=`file --mime-type -b "$file" | awk -F'/' '{print $1}'`
  if [ x$IMAGE_TYPE = "ximage" ]; then
      IMAGE_SIZE=`file -b $file | sed 's/ //g' | sed 's/,/ /g' | awk  '{print $2}'`
      WIDTH=`identify -format "%w" "$file"`
      HEIGHT=`identify -format "%h" "$file"`           
      # If the image width is greater that 200 or the height is greater that 150 a thumb is created
     if [ $WIDTH -ge  201 ] || [ $HEIGHT -ge 151 ]; then
        #This line convert the image in a 200 x 150 thumb 
        filename=$(realpath "$file")
        extension="${filename##*.}"
        filename="${filename%.*}"
        convert -sample 200x150 "$file" "${filename}_thumb.${extension}"   
     fi
  fi
done
