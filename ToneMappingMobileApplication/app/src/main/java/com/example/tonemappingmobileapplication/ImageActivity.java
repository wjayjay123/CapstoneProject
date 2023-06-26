package com.example.tonemappingmobileapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.OutputStream;
import java.util.Objects;

public class ImageActivity extends AppCompatActivity {

    ImageView convertedImgView;
    Button saveButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image);
        saveButton = (Button) findViewById(R.id.SaveButton);
        convertedImgView = (ImageView) findViewById(R.id.ConvertedImgView);

        Bitmap bmp = BitmapTransfer.bitmap;
        convertedImgView.setImageBitmap(bmp);

        saveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Bitmap bmp = ((BitmapDrawable)convertedImgView.getDrawable()).getBitmap();
                saveImage(bmp);
                Toast.makeText(ImageActivity.this, "Image Saved", Toast.LENGTH_SHORT).show();
            }
        });
    }

    void saveImage(Bitmap bmp){
        OutputStream fos;
        try{
            if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q){
                ContentResolver resolver = getContentResolver();
                ContentValues contentValues = new ContentValues();
                contentValues.put(MediaStore.MediaColumns.DISPLAY_NAME,"Image" + ".png");
                contentValues.put(MediaStore.MediaColumns.MIME_TYPE,"Image/png");
                Uri imgUri = resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,contentValues);
                fos = resolver.openOutputStream(Objects.requireNonNull(imgUri));
                bmp.compress(Bitmap.CompressFormat.PNG,100,fos);
                Objects.requireNonNull(fos);
            }
        }
        catch (Exception e){
            Log.d("Error",e.toString());
        }
    }
}