# Worked assessment example — Can a predicted vector be turned back into a picture?

## Goal

The v1 GRU baseline predicts, for every frame of a story, the CLIP-H vector of the **next** frame. In this example you freeze that model and train a small **decoder** (an MLP followed by transposed convolutions) that turns a 1024-number vector back into pixels: the three 64×64 crops of the next frame.

You train the same decoder four times, changing only the vector it is given:

| Name | Vector given to the decoder | What it tells you |
|---|---|---|
| `Z_true` | the real CLIP-H vector of frame *t+1* | the best this decoder can do |
| `Z_hat` | the vector the frozen model predicts for frame *t+1* | how good the prediction is |
| `Z_prev` | the real vector of frame *t* | what you get by repeating the last frame |
| `Z_shuf` | the real vector of a frame from another story | what you get with no information |

The result is a table of validation errors and a grid of pictures: the real crops on top, and the four reconstructions under them. The question to answer at the end is: **does the predicted vector give a better picture of the next frame than the previous frame's vector does?**

**Reference system:** `v1_gru_baseline.ipynb`, trained and still in memory.

**Dataset:** StoryReasoning packed features (vectors only); the pictures are downloaded from Hugging Face once, about 770 MB.

**Recommended runtime:** **GPU**. **Estimated time:** about 2 hours.

**Before you start.** Run every cell of the reference system. These names must exist: `model`, `img_store`, `clip_store`, `train_ids`, `val_ids`, `StorySequences`, `collate`, `to_device`, `val_loader`. Write down the validation `cosine` printed for the last training epoch.

Every Gemini chat response must begin with one label: `[BRAINSTORMING]`, `[MAIN]`, `[CLARIFICATION]`, `[CRITICAL]` or `[INTERPRETATION]`. If the label is missing, ask Gemini to reissue the response.

---

## Part 1 — Understand what you have

No prompts are given in this part. Write your own.

### Questions to answer with Gemini

Gemini can read your notebook cells but **cannot see `store.py`**, the file that loads the data. If you ask it how the store works, it will guess. Ask it instead to print the relevant source code (for example with `inspect.getsource`) and to answer from what was printed.

1. `clip_store[val_ids[0]][0].image` is `None` right now. Why, and what has to change when the store is created so that it returns a picture? Is `image` a method you call or an attribute you read?
2. One of the two stores has three crops per frame and the other has one. Which is which, where are the crop positions kept, and what do the four numbers of one crop window mean?
3. In the baseline, which tensor is the target of the image head, what is its shape, and which loss compares the prediction with it?

### Small code exercises

Write these yourself, one short cell each, without Gemini.

1. Take `f = clip_store[val_ids[0]][0]`. Print the shapes of `f.image_feat_crops` and `f.image_feat`.
2. Print `n_crops` and `img_dim` for `img_store` and for `clip_store`.
3. Print `f.crop_windows`, `f.width` and `f.height`. Do the windows overlap?
4. Use `np.allclose` to check that `f.image_feat` is the mean of the three rows of `f.image_feat_crops`.
5. Print the length (`np.linalg.norm`) of each crop vector and of their mean. Are they unit length?
6. Take one batch from `val_loader` and print the shapes of `batch["img"]` and `batch["z"]`. Which one does the model read, and which one does it try to predict?

---

## Part 2 — Load the pictures and show the three crops

Copy each prompt into Gemini, run the cell, and answer the questions before continuing.

## Prompt 1

> Rules for this conversation: you cannot see store.py, so use only attributes whose source code or output has been printed in this notebook, and ask me if you need another. Never write try/except, hasattr checks or silent fallbacks: if a value is None, the code must stop with a clear error.
>
> Re-create clip_store with exactly the same arguments as before plus hf_dataset="auto", so that pictures are downloaded from Hugging Face on first use. Then, for frames 0 and 1 of story val_ids[0], show in one figure the full picture with the three crop windows drawn as rectangles in three colours, and under it the three crops cut out with image.crop. Put the picture size in pixels in the title. Do not resize anything.

### Questions

1. Which part of the frame appears in two crops?
2. The target of the model is one vector for the whole frame. What is it a summary of?

## Prompt 2

> Write one function frame_crops(frame, size=64). It reads frame.image and frame.crop_windows, cuts the three windows out of the picture, resizes each crop to size x size pixels, and returns one uint8 tensor of shape [3, 3, size, size], meaning [crop, colour channel, height, width]. If frame.image or frame.crop_windows is None it must raise a ValueError with a clear message. Call it once on a frame of clip_store and print the shape, dtype, minimum and maximum. Briefly explain the meaning of the four dimensions.

### Test the function yourself

1. `assert` the shape and the dtype of the result.
2. `assert` that crop 0 and crop 2 are **not** identical (`torch.equal`). Three copies of the same picture would pass a shape test.
3. Show the three crops with `imshow` (matplotlib wants `[height, width, channel]`) and compare them with the figure from Prompt 1.
4. Call `frame_crops(img_store[val_ids[0]][0])`. It must raise a `ValueError`. Why can this store not give crops?

---

## Part 3 — Prepare the data and the validation function

## Prompt 3

> Create one code cell that builds the data for a decoding experiment by running the frozen model exactly once. Call model.eval(), work under torch.no_grad() and create no optimiser.
>
> Set N_TRAIN = 2000 and N_VAL = 300 and mark both with a TRY comment. Write build_cache(ids) and call it on train_ids[:N_TRAIN] and val_ids[:N_VAL] to get train_set and val_set.
>
> Inside build_cache, loop over DataLoader(StorySequences(ids), batch_size=16, shuffle=False, collate_fn=collate) and move each batch with to_device. Compute z_hat = model.image_head(model.encode(img[:, :-1], rows[:, :-1], tokens[:, :-1])) exactly as the evaluate function of the notebook does. For every story b of the batch and every position t that has a real frame t+1 (use frame_mask), append one row: Z_true = z[b, t+1], Z_hat = z_hat[b, t], Z_prev = z[b, t], X = frame_crops(clip_store[story_id][t+1]), story = story_id, frame = t+1.
>
> Return a dict with Z_true, Z_hat and Z_prev as CPU tensors [N, 1024], X as a CPU uint8 tensor [N, 3, 3, 64, 64], and story and frame as lists. Keep X as uint8 and never convert the whole of X to float. L2-normalise Z_true, Z_hat and Z_prev.
>
> Finally add Z_shuf: for each row, the Z_true of a random row that belongs to a DIFFERENT story (fixed seed), and a list shuf_story with the story that vector came from.
>
> Print every shape and the time taken. Mark with KEY comments the lines that decide which vector is paired with which picture.

### Questions

1. Every row pairs four vectors with the **same** picture. Which frame is the picture, and which frame does each vector come from?
2. Why is the model run once here, and not inside the decoder's training loop?

### Check the data yourself

1. Print the shape of every tensor in `val_set`.
2. Pick a row `i`. Show `val_set["X"][i]` next to `clip_store[story][frame].image` for that row's story and frame. Is it the same picture?
3. Print the mean cosine similarity on `val_set` of `Z_hat` with `Z_true`, of `Z_prev` with `Z_true`, and of `Z_shuf` with `Z_true`. The first number should match the validation `cosine` you wrote down. If it does not, the rows are misaligned.
4. `assert` that no row has `story == shuf_story`.

## Prompt 4

> Without defining or training any model yet, write the validation function we will use later, and test it with stand-in decoders.
>
> Write val_mse(decoder, key): the mean squared error over all of val_set between decoder(val_set[key]) and val_set["X"] / 255, computed in batches on the device under torch.no_grad().
>
> Write show_row(i, decoders), where decoders is a dict {name: (decoder, key)} and a decoder is anything that maps a batch of vectors [B, 1024] to pictures [B, 3, 3, 64, 64] with values between 0 and 1. It draws one figure for row i of val_set: the three target crops in the top row, then one row of three reconstructions per entry of the dict, each row labelled with its name and its MSE against the target. Put the story id and frame index in the title.
>
> To test both functions, compute mean_picture, the average of train_set["X"] / 255 over all rows (in chunks, never converting all of X to float at once), and define mean_decoder, a function that ignores its input and returns mean_picture repeated B times. Call show_row(5, decoders) with four entries named Z_true, Z_hat, Z_prev and Z_shuf that all use mean_decoder, and print val_mse(mean_decoder, "Z_true").

### Questions

1. What does the mean training picture look like? Why is it a useful reference for the decoders you will train?
2. The four test rows are identical. Why is that the correct output here?

### Test the validation function yourself

1. Write a stand-in decoder that returns the **real crops** of row `i` (from `val_set["X"]`), and pass it to `show_row`. The row must look exactly like the target and its MSE must be 0.
2. Write down the value of `val_mse(mean_decoder, "Z_true")`. A trained decoder that cannot beat this number has learned nothing from its input.

---

## Part 4 — Create the decoder and train it

## Prompt 5

> Create a short Markdown explanation and one code cell.
>
> Define ZDecoder: Linear(1024, 16384) and ReLU; reshape the 16384 values to [256, 8, 8]; three ConvTranspose2d layers with kernel 4, stride 2 and padding 1 going 256 -> 128 -> 64 -> 9 channels, with ReLU between them and Sigmoid at the end; reshape the output to [B, 3, 3, 64, 64].
>
> Define train_decoder(key, epochs=10, seed=0): call torch.manual_seed(seed), create a new ZDecoder on the device, use Adam with lr 1e-3 and shuffled mini-batches of 64 rows of train_set[key] and train_set["X"], converting each batch of X to float / 255 on the device; the loss is MSE. After every epoch print the epoch, the training MSE and val_mse(decoder, key), and keep them in a history list. Return the decoder and the history.
>
> Train ONE decoder only: dec_true, hist_true = train_decoder("Z_true"). Then call show_row(i, {"Z_true": (dec_true, "Z_true")}) for i in SHOW = [5, 200, 500].
>
> In the Markdown, briefly explain what the decoder takes in and gives out, what one transposed convolution does to the spatial size, and why the last layer has 9 channels.

### Questions

1. What survives in the reconstructions (colour, layout, objects, faces) and what does not?
2. Does validation MSE keep falling as long as training MSE does?

### Check the decoder yourself

1. Pass `torch.randn(5, 1024)` through a new `ZDecoder()` and print the output shape.
2. Print the number of parameters of each layer. Which layer holds most of them?

## Prompt 6

**Before running:** write down the order you expect for the four validation errors, best to worst.

> Without changing ZDecoder, val_mse, train_decoder or show_row, train three more decoders with the same seed and number of epochs: dec_hat on "Z_hat", dec_prev on "Z_prev" and dec_shuf on "Z_shuf". Print one table with a row for each of Z_true, Z_hat, Z_prev, Z_shuf and the constant mean picture, and columns: final training MSE, final validation MSE, best validation MSE and its epoch. Plot the four validation curves in one figure with the mean-picture error as a horizontal line. Then call show_row for each i in SHOW with all four trained decoders, each given its own kind of vector.

### Questions

1. Was your predicted order right? Which result surprised you most?
2. Where does the `Z_shuf` decoder end up compared with the mean picture? Look at its *training* error too: what is it learning?
3. Is the picture decoded from `Z_hat` better than the one decoded from `Z_prev`? Answer with the table and with the grids.

---

## Try it yourself manually

Without asking Gemini, go back to the **code cell generated by Prompt 6 in this experiment**. Change the `show_row` call so that the `Z_hat` row uses `dec_true`, the decoder trained on real vectors, instead of `dec_hat`. Then print `val_mse(dec_true, "Z_hat")` and `val_mse(dec_true, "Z_prev")` in a new cell.

Before running, predict: `Z_hat` is the model's best guess of `Z_true` and their cosine similarity is high. Will `dec_true` draw a reasonable picture from it?

- Is `val_mse(dec_true, "Z_hat")` better or worse than the mean picture?
- Compute the mean cosine similarity between different rows of `val_set["Z_hat"]`, and the same for `val_set["Z_true"]`. Which set of vectors is more spread out?
- What does this say about using one decoder for both real and predicted vectors?

---

## What the results mean

The decoder is a measuring instrument. Its error tells you how much about the pixels of frame *t+1* can be read out of a vector, and the four versions give that number a scale: `Z_true` is the ceiling, `Z_shuf` and the mean picture are the floor, `Z_prev` is the baseline to beat, and `Z_hat` is the model.

Expect blurred pictures even at the ceiling. One pooled vector does not hold the detail, and mean squared error is smallest for the *average* of all pictures that fit the vector. If your `Z_hat` decoder was no better than your `Z_prev` decoder, report it as it is: it is a result about the baseline model, and it agrees with the retrieval numbers the baseline printed next to `copy_last`.

Now ask Gemini:

> Using our table of validation MSE for the decoders trained on Z_true, Z_hat, Z_prev and Z_shuf, the mean-picture baseline, the picture grids, and the result of feeding Z_hat into dec_true, discuss what evidence we have that the model's predicted vector carries information about the next frame beyond what the previous frame already gives. Separate what the evidence shows from what it does not show. If Z_hat was not clearly better than Z_prev in our run, explain what that could mean instead of forcing a success story, and name one control we have not run.

### Final discussion questions

1. Why are four decoders needed? What could you conclude from the `Z_hat` decoder alone?
2. Why does MSE produce blurred pictures, and what kind of decoder would you need for sharp ones?
3. A decoder can read information out of a vector. Why is that not proof that the model uses that information?
4. Which limitations would you list for this investigation (data used, seeds, picture size, error measure)?

## When Gemini goes wrong

- **It uses a name you have never seen printed.** Ask which printed line supports it, and print the source if none does.
- **A loss is exactly 0, or nothing is displayed.** Something is being skipped. Look for `try/except` or an `if` that silently continues, and have it removed so the real error appears.
- **Training is very slow.** A picture is being loaded inside the training loop. Pictures are read once, in Prompt 3.
- **The session runs out of memory.** All of `X` was converted to float. Keep `X` as `uint8`, convert one batch at a time, or lower `N_TRAIN`.
