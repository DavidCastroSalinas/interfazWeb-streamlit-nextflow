process analyze {
    input:
    path input_file
    path output_dir

    output:
    path "${output_dir}/result1.txt"

    script:
    """
    mkdir -p $output_dir
    
    cat $input_file > $output_dir/result1.txt
    """
 
}
