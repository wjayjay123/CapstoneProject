function [ labels, mdata, edges ] = quantizeNL_float( y, nclust, lum )
% y is input data
% nclust is the number of clusters or quantization levels. If you want to
% quantize data with b bits then nclust <= 2^b (256 if b=8)
% labels are the quantization intervals in [1, nclust] range assigned to y
% mdata is the mean value of each cluster

lum = double(lum);
lum0 = lum;
lum = reshape(lum, 1, numel(lum));
lum = sort(lum);

y = double(y);
y = reshape(y, 1, numel(y));
y = sort(y);

edges = [0,numel(y)];
errors = sum((y-mean(y)).^2);

s_data = cumsum(y);
ss_data = cumsum(y.^2);

for i = 1 : nclust-1
    [~,idx] = max(errors);
    k = edges(idx); n = edges(idx+1)-k;
    sn = s_data(k+n); if(k>=1) sn = sn - s_data(k); end
    ssn = ss_data(k+n); if(k>=1) ssn = ssn - ss_data(k); end
    d = 2; m = floor(n/d);
    while(1)
        sm = s_data(k+m); if(k>=1) sm = sm - s_data(k); end
        ssm = ss_data(k+m); if(k>=1) ssm = ssm - ss_data(k); end
        e1 = ssm-sm^2/m;
        e2 = ssn - ssm - (sn - sm)^2/(n-m);
        d = 2 * d;
        if(abs(e1-e2) < 0.001 || d >= n)
            lum1 = median(lum(k+1:k+m)); lum2 = median(lum(k+m+1:k+n));
            delta1 = 10.^tvi(log10(lum1)); delta2 = 10.^tvi(log10(lum2));
            [~, lum_loc] = min(abs(delta1./(delta1+delta2) .* (lum(k+n)-lum(k+1)) + lum(k+1) - lum(k+1:k+n)));
            m = lum_loc;
            sm = s_data(k+m); if(k>=1) sm = sm - s_data(k); end
            ssm = ss_data(k+m); if(k>=1) ssm = ssm - ss_data(k); end
            e1 = ssm-sm^2/m;
            e2 = ssn - ssm - (sn - sm)^2/(n-m);
            
            edges = [edges(1:idx),k+m,edges(idx+1:end)];
            errors = [errors(1:idx-1),e1,e2,errors(idx+1:end)];
            break;
        else
            if(e1 > e2) m = m-floor(n/d); elseif(e1 < e2) m = m+floor(n/d); end
        end
    end
end

mdata = zeros(1, nclust);
mdata(1) = min(lum0(:));
mdata(end) = max(lum0(:));
for i=2:nclust-1
    if lum(edges(i))==lum(edges(i+1))
        ind = (lum0==lum(edges(i)));
        mdata(i) = mean(lum0(ind))+eps*i;
    else
        ind = (lum0>lum(edges(i)) & lum0<=lum(edges(i+1)));
        mdata(i) = mean(lum0(ind));
    end
end

labels_mdata = linspace(1, 256, nclust);
labels = interp1(mdata, labels_mdata, lum0, 'linear');

end