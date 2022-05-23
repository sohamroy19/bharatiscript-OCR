def char_resize(A):
    # [x,y]=size(A);
    # if x>y
    #     num=1;
    #     A=imresize(A, [24 NaN]);
    #     [x,y] = size(A);
    #     A = padarray(A, [floor((28-x)/2) floor((28-y)/2)]);
    #     [x,y]=size(A);
    #     if x~=28
    #         A=padarray(A, [28-x 0],'replicate', 'post');
    #     end
    #     if y~=28
    #         A=padarray(A, [0 28-y],'replicate', 'post');
    #     end
    # else
    #     num=2;
    #     A=imresize(A, [NaN 24]);
    #     [x,y] = size(A);
    #     A = padarray(A, [floor((28-x)/2) floor((28-y)/2)]);
    #     [x,y]=size(A);
    #     if x~=28
    #         A=padarray(A, [28-x 0],'replicate', 'post');
    #     end
    #     if y~=28
    #         A=padarray(A, [0 28-y],'replicate', 'post');
    #     end
    # end
    # output=A;
    # end

    # return output, num
    return A, 1
