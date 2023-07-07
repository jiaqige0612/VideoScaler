function imgo = NEDI(frame)

%frame = imread('0853x4.png');
figure;
imshow(frame);

tic;
m = 5; % window size
s = 2; % 1/2 of scale size

for iter = 1:s
    if iter == 1
        dims = size(frame);
    else
        dims = size(imgo);
    end
    rows = dims(1);
    cols = dims(2);
    targetSize = [2*rows, 2*cols];
    
    
    % Canny edge detection
    if iter ==1
        img=im2double(frame);
    else
        img=im2double(imgo);
    end
    
    I=rgb2gray(img);
    
    sharp = edge(I,'canny', 0.3); %Could you please also estimate when using sobel/prewitt instead of canny edge detection
    figure;
    imshow(sharp);
    
    
    % insert low-resolution pixels
    imgo = imresize(img, targetSize, 'bicubic'); %Could you please also estimate when using bicubic instead of lanczos3
    

    y = double(zeros(m^2, 1)); % pixels in the window
    C = double(zeros(m^2, 4)); % interpolation neighbours of each pixel in the window

    %% step 1  reconstruct the points with the form of (2*i+1,2*j+1)
    for k=1:3  % 3 colors
        for i=4:rows-4
            for j=4:cols-4
                if(sharp(i,j)==1)
                    temp=1;
                    for ii=(i+1-ceil(m/2)):(i+floor(m/2))
                       for jj=j+1-ceil(m/2):j+floor(m/2)
                           y(temp)=imgo(2*ii,2*jj,k);
                           C(temp,1)=imgo(2*ii-2,2*jj-2,k);
                           C(temp,2)=imgo(2*ii+2,2*jj-2,k);
                           C(temp,3)=imgo(2*ii+2,2*jj+2,k);
                           C(temp,4)=imgo(2*ii-2,2*jj+2,k);
                           temp=temp+1;                     
                       end
                    end
                    alpha = pinv(C' * C) * C' * y;
                    imgo(2*i+1,2*j+1,k)=(alpha(1)*imgo(2*i,2*j,k)+alpha(2)*imgo(2*i+2,2*j,k)...
                        +alpha(3)*imgo(2*i+2,2*j+2,k)+alpha(4)*imgo(2*i,2*j+2,k));
                        
                end
            end
        end 
    end
    
    
    %% step 2 reconstructed the points with the forms of (2*i+1,2*j)
    for k=1:3  % 3 colors
        for i=4:rows-4
            for j=4:cols-4
                if(sharp(i,j)==1)
                    temp=1;
                    for ii=(i+1-ceil(m/2)):(i+floor(m/2))
                       for jj=j+1-ceil(m/2):j+floor(m/2)
                           y(temp)=imgo(2*ii+1,2*jj-1,k);
                           C(temp,1)=imgo(2*ii-1,2*jj-1,k);
                           C(temp,2)=imgo(2*ii+1,2*jj-3,k);
                           C(temp,3)=imgo(2*ii+3,2*jj-1,k);
                           C(temp,4)=imgo(2*ii+1,2*jj+1,k);
                           temp=temp+1;                     
                       end
                    end
                    alpha = pinv(C' * C) * C' * y;
                    imgo(2*i+1,2*j,k)=(alpha(1)*imgo(2*i,2*j,k)+alpha(2)*imgo(2*i+1,2*j-1,k)...
                        +alpha(3)*imgo(2*i+2,2*j,k)+alpha(4)*imgo(2*i+1,2*j+1,k));
                end
            end
        end  
    end
    
    %% step 3 reconstructed the points with the forms of (2*i,2*j+1)
    
    for k=1:3  % 3 colors
        for i=4:rows-4
            for j=4:cols-4
                if(sharp(i,j)==1)
                    temp=1;
                    for ii=(i+1-ceil(m/2)):(i+floor(m/2))
                       for jj=j+1-ceil(m/2):j+floor(m/2)
                           y(temp)=imgo(2*ii+1,2*jj-1,k);
                           C(temp,1)=imgo(2*ii-1,2*jj-1,k);
                           C(temp,2)=imgo(2*ii+1,2*jj-3,k);
                           C(temp,3)=imgo(2*ii+3,2*jj-1,k);
                           C(temp,4)=imgo(2*ii+1,2*jj+1,k);
                           temp=temp+1;                     
                       end
                    end
                    alpha = pinv(C' * C) * C' * y;
                    imgo(2*i,2*j+1,k)=(alpha(1)*imgo(2*i-1,2*j+1,k)+alpha(2)*imgo(2*i,2*j,k)...
                        +alpha(3)*imgo(2*i+1,2*j+1,k)+alpha(4)*imgo(2*i,2*j+2,k));
                end
            end
        end  
    end
end