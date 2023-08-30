#!/bin/bash

search_string="000.36.63.H49.*"

search_string_pdf="$search_string.pdf"

replace_string='s/000\.36\.63\.H49\./000.032.63.H49./'


echo "----------- BAT DAU --------------"
echo $(date) ": Bat dau doi TEN THU MUC" 
find -type d -name "$search_string" -print0 | while read -d $'\0' file
do
    new_file="$(echo "$file" | sed "$replace_string")"
    mv "$file" "$new_file"
    echo $(date) ": $file => $new_file"
done
echo $(date) ": Doi TEN THU MUC xong"
echo "--------------------------------------------------"
echo "--------------------------------------------------"
echo $(date) ": Bat dau doi TEN FILE" 
find -type f -name "$search_string_pdf" -print0 | while read -d $'\0' file
do
    new_file="$(echo "$file" | sed "$replace_string")"
    mv "$file" "$new_file"
    echo $(date) ": $file => $new_file"
done
echo $(date) ": Doi TEN FILE xong" 
echo "----------- KET THUC --------------"

