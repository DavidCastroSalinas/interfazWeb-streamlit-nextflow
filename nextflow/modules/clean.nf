process clean {
    input:
    path input_file
    path output_dir

    output:
    path "${output_dir}/result2.txt"

    script:
    """


    cat $input_file > $output_dir/result2.txt
    """
}
