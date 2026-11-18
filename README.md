# AIO_TV PCM Tap Android Build

This repository builds Media Kit's Android `libmpv.so` with the AIO_TV PCM Tap patch for both `arm64-v8a` and `armeabi-v7a`.

## Required patch

Before running the workflow, add the verified patch file at:

`patches/mpv/0001-pcm-tap.patch`

The patch must be the exact file generated and validated from the prototype MPV source. The workflow checks that it exists and stops safely if it is missing.

## Build

Open **Actions → Build PCM Tap MPV → Run workflow**.

The workflow uses the official `media-kit/libmpv-android-video-build` build scripts and pins the MPV revision used by the prototype. It runs only the default flavor and uploads the four ABI JARs as an artifact. It does not publish a release or modify the AIO_TV app repository.

## Output

- `default-arm64-v8a.jar`
- `default-armeabi-v7a.jar`
- `default-x86.jar`
- `default-x86_64.jar`

Only ARM64 and ARM32 are intended for the PCM Tap runtime test.