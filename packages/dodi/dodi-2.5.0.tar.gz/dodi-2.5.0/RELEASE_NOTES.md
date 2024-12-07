## 2.5.0
Explicit Django 5 support

## 2.4.0
Explicit Pillow 10,11 support

## 2.3.0
Add type annotations

## 2.2.0
Support relative width/height cropping values

### 2.1.2
Percent-decode querystring when parsing

### 2.1.1
Respond appropriately to empty transform

## 2.1.0
Explicit django 4 support

### 2.0.2
Explicit Pillow 9 support

### 2.0.1
Documented stricter Pillow requirements, since 7.2.0 -> 8.2.* all fail one of our tests

# 2.0.0
Changed url format (put source in querystring, rather than path), 
to avoid issue with apache removing empty segments from url paths.

Backward compatible with 1.x iff you always use our utils for url generation 
(you'll need to adjust if you manually generate urls).

### 1.0.1
Explicit Django 2.2 support

# 1.0.0