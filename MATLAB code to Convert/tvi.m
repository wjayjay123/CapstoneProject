function threshold = tvi(intensity)
%---------------------------------------
% The output is the sensitivity of HVS measured as just noticeable
% difference in the ambient intensity defined by the input parameter.
%
% intensity: real luminance in log10 domain
% threshold: in log10 domain, delta(lum)=10.^(threshold)

threshold = zeros(size(intensity));

idx = find(intensity < -3.94);
threshold (idx) = -2.86;

idx = find(intensity >= -3.94 & intensity < -1.44);
threshold (idx) = (0.405 * intensity(idx) + 1.6) .^ 2.18 - 2.86;

idx = find(intensity >= -1.44 & intensity < -0.0184);
threshold (idx) = intensity(idx) - 0.395;

idx = find(intensity >= -0.0184 & intensity < 1.9);
threshold(idx) = (0.249 * intensity(idx) + 0.65) .^ 2.7 - 0.72;

idx = find(intensity >= 1.9);
threshold (idx) = intensity(idx) - 1.255;

threshold = threshold - 0.95;
end