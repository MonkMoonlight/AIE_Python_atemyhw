import tensorflow as tf
tf.get_logger().setLevel('ERROR')
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Grad-CAM helpers ---
def get_last_conv_layer(model):
    preferred = ["Conv_1", "out_relu"]
    by_name = {layer.name: layer for layer in model.layers}
    for name in preferred:
        if name in by_name:
            return by_name[name]
    for layer in reversed(model.layers):
        try:
            out_shape = layer.output_shape
        except Exception:
            continue
        if isinstance(out_shape, tuple) and len(out_shape) == 4:
            return layer
    raise ValueError("No suitable conv layer found for Grad-CAM.")

def make_gradcam_heatmap(img_array_batched, model, conv_layer_name=None, class_index=None):
    conv_layer = (model.get_layer(conv_layer_name) if conv_layer_name
                  else get_last_conv_layer(model))
    grad_model = tf.keras.models.Model([model.inputs],
                                       [conv_layer.output, model.output])
    with tf.GradientTape() as tape:
        conv_outputs, preds = grad_model(img_array_batched)
        if class_index is None:
            class_index = tf.argmax(preds[0])
        class_channel = preds[:, class_index]
    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(tf.multiply(conv_outputs, pooled_grads), axis=-1)
    heatmap = tf.maximum(heatmap, 0)
    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy().astype("float32")

def overlay_heatmap_on_image(orig_img_path, heatmap, output_path, alpha=0.4):
    orig = image.load_img(orig_img_path)
    orig_arr = image.img_to_array(orig).astype("uint8")
    h, w = orig_arr.shape[:2]
    heatmap_resized = tf.image.resize(heatmap[..., None], (h, w)).numpy().squeeze()
    plt.figure(figsize=(6, 6))
    plt.imshow(orig_arr)
    plt.imshow(heatmap_resized, cmap="jet", alpha=alpha)
    plt.axis("off")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()


model = MobileNetV2(weights="imagenet")

def classify_image(image_path):
    try:
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predictions = model.predict(img_array, verbose=0)
        decoded_predictions = decode_predictions(predictions, top=3)[0]

        print("\nTop-3 Predictions for", image_path)
        for i, (_, label, score) in enumerate(decoded_predictions):
            print(f"  {i + 1}: {label} ({score:.2f})")
            
# --- Grad-CAM for top-1 class ---
        top1_class_index = int(np.argmax(predictions[0]))
        heatmap = make_gradcam_heatmap(
            img_array, model, conv_layer_name=None, class_index=top1_class_index
        )
        base, _ = os.path.splitext(image_path)
        gradcam_path = f"{base}_gradcam.png"
        overlay_heatmap_on_image(image_path, heatmap, gradcam_path, alpha=0.4)
        print(f"Grad-CAM saved to: {gradcam_path}")
        
    except Exception as e:
        print(f"Error processing '{image_path}': {e}")

if __name__ == "__main__":
    print("Image Classifier (type 'exit' to quit)\n")
    while True:
        image_path = input("Enter image filename: ").strip()
        if image_path.lower() == "exit":
            print("Goodbye!")
            break
        classify_image(image_path)


