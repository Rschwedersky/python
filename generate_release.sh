do_build_and_push_nginx(){
    TAG=$2
    if [ -z "$TAG" ]
    then
        echo "Please, provide TAG with version, for example:"
        echo "bash generate_release build_and_push_nginx v1.5.0"
        print_help;
    else
        echo "Building Hub App Version 🔥🔥 $TAG 🔥🔥"
        sleep 3
        aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin 526932095279.dkr.ecr.us-east-1.amazonaws.com
        docker build -t 526932095279.dkr.ecr.us-east-1.amazonaws.com/manager-proxy:$TAG ./nginx
        docker push 526932095279.dkr.ecr.us-east-1.amazonaws.com/manager-proxy:$TAG
    fi
}

do_build_and_push_hub(){
    TAG=$2
    if [ -z "$TAG" ]
    then
        echo "Please, provide TAG with version, for example:"
        echo "bash generate_release do_build_and_push_hub v1.5.0"
        print_help;
    else
        echo "Building Hub App Version 🔥🔥 $TAG 🔥🔥"
        sleep 3
        aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin 526932095279.dkr.ecr.us-east-1.amazonaws.com
        docker build -t 526932095279.dkr.ecr.us-east-1.amazonaws.com/manager:$TAG .
        docker push 526932095279.dkr.ecr.us-east-1.amazonaws.com/manager:$TAG
    fi
}

process_arguments(){
    while [ -n "$1" ]
    do
        case $1 in
            -h|--help) print_help; exit 1;;
            build_and_push_hub) do_build_and_push_hub $@; shift; break ;;
            build_and_push_nginx) do_build_and_push_nginx $@; shift; break ;;
        esac
        echo print_help; shift
    done
}


process_arguments "$@"