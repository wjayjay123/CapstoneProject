function ldrImg = DCA_TMO(hdrImg)

%% set parameters
K = 55;

%% pre-processing
% [N, M, C] = size(hdrImg);
maxhdr = MaxQuart(hdrImg(:), 0.99);
minhdr = MaxQuart(hdrImg(:), 0.01);
hdrImg(hdrImg>maxhdr) = maxhdr;
hdrImg(hdrImg<minhdr) = minhdr;

%% tone map using clustering method
hdrLum = 0.2126 * hdrImg(:,:,1) + 0.7152 * hdrImg(:,:,2) + 0.0722 * hdrImg(:,:,3);
hdrLum1 = hdrLum./max(hdrImg(:));
hdrPQ = ((107/128 + 2413/128*hdrLum1.^(1305/8192)) ./ (1 + 2392/128*hdrLum1.^(1305/8192))) .^ (2523/32);
[labels, ~, ~] = quantizeNL_float(hdrPQ, K, hdrLum);

%% local enhancemant using DoG
sigmaC = 0.5;
sigmaS = 0.8;
window = 9;
gfilterC = fspecial('gaussian', window, sigmaC);
gfilterS = fspecial('gaussian', window, sigmaS);
DoGfilter = gfilterC - gfilterS;
hdrPQnor = 255 .* (hdrPQ - min(hdrPQ(:))) ./ (max(hdrPQ(:)) - min(hdrPQ(:))) + 1;
hdrPQnor = hdrPQnor .* 0.35 + labels .* 0.65;
labels_DoG = labels + 3.0*imfilter(hdrPQnor, DoGfilter, 'replicate');

%% color restoration
s1 = (labels_DoG - min(labels_DoG(:))) ./ (max(labels_DoG(:)) - min(labels_DoG(:)));
s = 1 - atan(s1);
s = min(s, 0.5);
ldrImg_DoG = (hdrImg ./ hdrLum).^s .* labels_DoG;
maxx = MaxQuart(ldrImg_DoG(:), 0.99);
minn = MaxQuart(ldrImg_DoG(:), 0.01);
if maxx<255
    if max(ldrImg_DoG(:))<255
        maxx = max(ldrImg_DoG(:));
    else
        maxx = 255;
    end
end
if minn>0
    if min(ldrImg_DoG(:))>0
        minn = min(ldrImg_DoG(:));
    else
        minn = 0;
    end
end
ldrImg_DoG(ldrImg_DoG>maxx) = maxx;
ldrImg_DoG(ldrImg_DoG<minn) = minn;
ldrImg = 255.* ((ldrImg_DoG - minn) ./ (maxx - minn));

end

