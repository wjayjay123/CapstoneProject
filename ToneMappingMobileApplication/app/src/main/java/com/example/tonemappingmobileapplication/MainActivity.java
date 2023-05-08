package com.example.tonemappingmobileapplication;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContentResolverCompat;
import androidx.core.content.ContextCompat;

import android.app.Activity;
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
import android.widget.TextView;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Objects;

public class MainActivity extends AppCompatActivity {

    TextView textView;
    Button submitButton;
    Button saveButton;
    Button browseButton;
    ImageView imageView;
    byte[] fileData;
    final int fileRequestCode = 99;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = (TextView) findViewById(R.id.TextViewTest);
        submitButton = (Button) findViewById(R.id.ButtonTest);
        saveButton  = (Button) findViewById(R.id.ButtonSave);
        browseButton = (Button) findViewById(R.id.ButtonBrowse);
        imageView = (ImageView) findViewById(R.id.ImageViewTest);

        //Start Python
        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        //Create Python instance
        Python py = Python.getInstance();

        browseButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent filePickerIntent = new Intent(Intent.ACTION_GET_CONTENT);
                filePickerIntent.setType("*/*");
                startActivityForResult(filePickerIntent,fileRequestCode);
            }
        });

        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //Create Python Object
                PyObject pythonObj = py.getModule("main"); //Python script name as input parameter
                //Call Python Function
                PyObject obj = pythonObj.callAttr("main",fileData); //Python function name as input parameter
                String imgStr = obj.toString();
                byte data [] = android.util.Base64.decode(imgStr, Base64.DEFAULT);
                Bitmap bmp = BitmapFactory.decodeByteArray(data,0,data.length);
                imageView.setImageBitmap(bmp);
            }
        });

        saveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Bitmap bmp = ((BitmapDrawable)imageView.getDrawable()).getBitmap();
                saveImage(bmp);
                Toast.makeText(MainActivity.this, "Image Saved", Toast.LENGTH_SHORT).show();
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(requestCode == fileRequestCode && resultCode == Activity.RESULT_OK){
            if(data == null){
                return;
            }
            Uri fileUri = data.getData();
            try {
                InputStream fileInput = getContentResolver().openInputStream(fileUri);
                fileData = getBytes(fileInput);
            } catch (IOException e) {
                e.printStackTrace();
            }
            textView.setText(fileData.toString());
        }
    }

    public byte[] getBytes(InputStream inputStream) throws IOException {
        ByteArrayOutputStream byteBuffer = new ByteArrayOutputStream();
        int bufferSize = 1024;
        byte[] buffer = new byte[bufferSize];

        int len = 0;
        while ((len = inputStream.read(buffer)) != -1) {
            byteBuffer.write(buffer, 0, len);
        }
        return byteBuffer.toByteArray();
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
