% clear all; clc;

DatasetLocation = 'HDRim/';
% EXRfiles = dir([DatasetLocation, '*.exr']);
%EXRfiles = dir([DatasetLocation, '*.hdr']);
EXRfiles = dir([DatasetLocation, 'moto.hdr']);
len = length(EXRfiles);

for i = 1:len
    EXRfile_name = EXRfiles(i).name;
    loc = strfind(EXRfile_name, '.');
    name = EXRfile_name(1:loc-1);
%     hdrImg = read_exr([DatasetLocation, EXRfile_name]);
    hdrImg = double(hdrread([DatasetLocation, EXRfile_name]));
    disp(hdrImg(1,1,1))
    hdrImg(hdrImg<=0) = eps;
   
    ldrImg = DCA_TMO(hdrImg);
    imwrite(uint8(ldrImg), ['LDRim\', name, '.png'])
    imshow(uint8(ldrImg))
    
    i
end


% hdrImg = double(hdrread('moto.hdr'));
% hdrImg = (hdrImg - min(hdrImg)) ./ (max(hdrImg) - min(hdrImg));
% figure(1);imshow(hdrImg)
% hdrImg_tm = tonemap(hdrImg);
% figure(2);imshow(hdrImg_tm)

