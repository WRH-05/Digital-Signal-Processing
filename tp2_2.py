import numpy as np
import matplotlib.pyplot as plt
import cv2
import skimage.io as io
from dct import dct_2d

# Read image
img=io.imread("lena.jpg",as_gray=True)

# Obtaining a mask through zigzag scanning
def z_scan_mask(C,N):
    mask=np.zeros((N,N))
    start=0
    mask_m=start
    mask_n=start
    for i in range(C):
        if i==0:
            mask[mask_m,mask_n]=1
        else:
            # If even, move upward to the right
            if (mask_m+mask_n)%2==0:
                mask_m-=1
                mask_n+=1
                # If it exceeds the upper boundary, move downward
                if mask_m<0:
                    mask_m+=1
                # If it exceeds the right boundary, move left
                if mask_n>=N:
                    mask_n-=1
            # If odd, move downward to the left
            else:
                mask_m+=1
                mask_n-=1
                # If it exceeds the lower boundary, move upward
                if mask_m>=N:
                    mask_m-=1
                # If it exceeds the left boundary, move right
                if mask_n<0:
                    mask_n+=1
            mask[mask_m,mask_n]=1
    return mask

# overlaying the mask, discarding the high-frequency components
def Compress(img,mask,N):
    img_dct=np.zeros((img.shape[0]//N*N,img.shape[1]//N*N))
    for m in range(0,img_dct.shape[0],N):
        for n in range(0,img_dct.shape[1],N):
            # pos_m=m*N
            # pos_n=n*N
            # DCT_v=DCT[m,:].reshape(-1,1)
            # DCT_T_h=DCT.T[:,n].reshape(-1,N)
            block=img[m:m+N,n:n+N]
            print(block.shape)
            # DCT
            # basis[pos_m:pos_m+N,pos_n:pos_n+N]=np.matmul(DCT_v,DCT_T_h)
            coeff=cv2.dct(block)
            # coeff=block*DCT
            # Center values
            # coeff+=np.absolute(np.amin(coeff))
            # scale=np.around(1/np.amax(coeff),decimals=3)
            # for m1 in range(coeff.shape[0]):
                # for n1 in range(coeff.shape[1]):
                    # coeff[m1][n1]=np.around(coeff[m1][n1]*scale,decimals=3)
            # IDCT, but only the parts of the image where the mask has a value of 1 are retained
            print(coeff.shape)
            print()
            iblock=cv2.idct(coeff*mask)
            # iblock=cv2.idct(coeff)
            img_dct[m:m+N,n:n+N]=iblock
    return img_dct

# Define functions to compute Mean Squared Error and PSNR
def compute_mse(original, compressed):
    return np.mean((original - compressed) ** 2)

def compute_psnr(original, compressed):
    mse = compute_mse(original, compressed)
    if mse == 0:
        return float('inf')
    max_pixel = 1.0  # assuming the image is normalized between 0 and 1
    return 20 * np.log10(max_pixel / np.sqrt(mse))

# Generate compressed images with different numbers of retained coefficients
img_1  = Compress(img, z_scan_mask(1, 8), 8)
img_3  = Compress(img, z_scan_mask(3, 8), 8)
img_10 = Compress(img, z_scan_mask(10, 8), 8)

# Compute MSE and PSNR for each compressed image
mse_1  = compute_mse(img, img_1)
psnr_1 = compute_psnr(img, img_1)
mse_3  = compute_mse(img, img_3)
psnr_3 = compute_psnr(img, img_3)
mse_10  = compute_mse(img, img_10)
psnr_10 = compute_psnr(img, img_10)

# show MSE and PSNR values
print(f"MSE for 1 coefficient: {mse_1:.4f}, PSNR: {psnr_1:.2f} dB")
print(f"MSE for 3 coefficients: {mse_3:.4f}, PSNR: {psnr_3:.2f} dB")
print(f"MSE for 10 coefficients: {mse_10:.4f}, PSNR: {psnr_10:.2f} dB")

# Images keeping only 1, 3, and 10 low-frequency coefficients
plt.figure(figsize=(16, 4))
plt.gray()

plt.subplot(141)
plt.title('Original image')
plt.imshow(img)
plt.axis('off')

plt.subplot(142)
plt.title('Keep 1 coefficient')
plt.imshow(img_1)
#plt.axis('off')
plt.xlabel(f"MSE: {mse_1:.4f}\nPSNR: {psnr_1:.2f} dB")

plt.subplot(143)
plt.title('Keep 3 coefficients')
plt.imshow(img_3)
#plt.axis('off')
plt.xlabel(f"MSE: {mse_3:.4f}\nPSNR: {psnr_3:.2f} dB")

plt.subplot(144)
plt.title('Keep 10 coefficients')
plt.imshow(img_10)
#plt.axis('off')
plt.xlabel(f"MSE: {mse_10:.4f}\nPSNR: {psnr_10:.2f} dB")
plt.show()
