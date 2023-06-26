package com.example.tonemappingmobileapplication;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContract;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContentResolverCompat;
import androidx.core.content.ContextCompat;
import androidx.documentfile.provider.DocumentFile;
import androidx.loader.content.CursorLoader;

import android.Manifest;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.icu.util.Output;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.storage.StorageManager;
import android.os.storage.StorageVolume;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.provider.OpenableColumns;
import android.provider.Settings;
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

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.List;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity {

    TextView textView;
    Button submitButton;
    Button browseButton;
    String fileExt = "";
    String destFileName = "";
    final int fileRequestCode = 99;
    final int STORAGE_PERMISSION_CODE = 100;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = (TextView) findViewById(R.id.InfoTextView);
        submitButton = (Button) findViewById(R.id.ConvertButton);
        browseButton = (Button) findViewById(R.id.ButtonBrowse);

        ActivityCompat.requestPermissions(this, new String[]{
                Manifest.permission.WRITE_EXTERNAL_STORAGE,
                Manifest.permission.READ_EXTERNAL_STORAGE},
                PackageManager.PERMISSION_GRANTED
        );

        //Start Python
        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        //Create Python instance
        Python py = Python.getInstance();

        browseButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(checkPermission()){
                    Intent filePickerIntent = new Intent(Intent.ACTION_GET_CONTENT);
                    filePickerIntent.setType("*/*");
                    startActivityForResult(filePickerIntent,fileRequestCode);
                }else{
                    requestPermissions();
                }
            }
        });

        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //Create Python Object
                PyObject pythonObj = py.getModule("main"); //Python script name as input parameter
                //Call Python Function
                PyObject obj = pythonObj.callAttr("main", destFileName); //Python function name as input parameter
                String imgStr = obj.toString();
                byte data [] = android.util.Base64.decode(imgStr, Base64.DEFAULT);
                Bitmap bmp = BitmapFactory.decodeByteArray(data,0,data.length);
                BitmapTransfer.bitmap = bmp;
                Intent intent = new Intent(MainActivity.this, ImageActivity.class);
                startActivity(intent);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(requestCode == fileRequestCode && resultCode == Activity.RESULT_OK){
            if(data != null && data.getData() != null){
                Uri fileUri = data.getData();
                Cursor fileCursor = getContentResolver().query(fileUri, null, null, null, null);
                int nameIndex = fileCursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                fileCursor.moveToFirst();
                String fileName = fileCursor.getString(nameIndex);
                String fileExt = getExt(fileName);
                textView.setText(fileName);
                copyFile(fileName, fileExt);
            }else{
                Toast.makeText(MainActivity.this, "File is empty",Toast.LENGTH_SHORT);
            }
        }
    }

    public void requestPermissions(){
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.R){
            try{
                Log.d("debug", "requestpermission:try");
                Intent intent = new Intent(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION);
                Uri permissionURI = Uri.fromParts("package", this.getPackageName(), null);
                intent.setData(permissionURI);
                storageActivityResultLauncher.launch(intent);
            }catch (Exception e){
                Log.d("debug", "requestpermission:catch");
                Intent intent = new Intent();
                intent.setAction(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION);
                storageActivityResultLauncher.launch(intent);
            }
        }else{
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.READ_EXTERNAL_STORAGE},STORAGE_PERMISSION_CODE);
        }
    }

    private ActivityResultLauncher<Intent> storageActivityResultLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    Log.d("Debug", "onActivityResult: Permissions");
                    if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.R){
                        if(Environment.isExternalStorageManager()){
                            Log.d("Debug", "External Storage Permission is granted");
                        }else{
                            Toast.makeText(MainActivity.this, "Please enable external storage permission", Toast.LENGTH_SHORT).show();
                        }
                    }
                }
            }
    );

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if(requestCode == STORAGE_PERMISSION_CODE){
            if(grantResults.length > 0){
                boolean write = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                boolean read = grantResults[1] == PackageManager.PERMISSION_GRANTED;

                if(write && read){
                    Log.d("Debug", "External Storage Permissions Granted");
                }else{
                    Toast.makeText(MainActivity.this, "Please enable external storage permission", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }

    public boolean checkPermission(){
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.R){
            return Environment.isExternalStorageManager();
        }else{
            int write = ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE);
            int read = ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE);
            return write == PackageManager.PERMISSION_GRANTED && read == PackageManager.PERMISSION_GRANTED;
        }
    }

    public void copyFile(String fileName, String fileExt){

        StorageManager storageManager = (StorageManager) getSystemService(STORAGE_SERVICE);
        List<StorageVolume> storageVolumeList = storageManager.getStorageVolumes();

        StorageVolume storageVolume = storageVolumeList.get(0);

        File filesource = new File(storageVolume.getDirectory().getPath() + "/Download/" + fileName);
//        textView.setText(storageVolume.getDirectory().getPath());
        destFileName = "temp" + fileExt;
        File filedestination = new File(getFilesDir().toString() + "/chaquopy/AssetFinder/app",destFileName);

        try{
            InputStream inputStream = new FileInputStream(filesource);
            OutputStream outputStream = new FileOutputStream(filedestination);

            byte[] byteArrayBuffer = new byte[1024];
            int intLength;
            while((intLength = inputStream.read(byteArrayBuffer)) > 0){
                outputStream.write(byteArrayBuffer,0,intLength);
            }
            inputStream.close();
            outputStream.close();

        }catch (Exception e){
            textView.setText("Error: " + e.toString());
        }
    }

    public String getExt(String fileName){
        String patternString = "\\.([a-zA-Z0-9]+)$";
        Pattern pattern = Pattern.compile(patternString);
        Matcher matcher = pattern.matcher(fileName);
        if (matcher.find()) {
            String extension = matcher.group(1);
            return "." + extension;
        }else{
            return "";
        }
    }
}
