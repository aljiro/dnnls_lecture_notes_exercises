# Worked assessment example — Can a predicted vector be turned back into a picture?

**Reference system:** `v1_gru_baseline.ipynb`, trained and still in memory.

**Dataset:** StoryReasoning, Hugging Face *train* split (3,552 stories, 44,199 frames), split by story into train and validation as in the baseline. The packed features hold vectors only; the pictures are fetched from Hugging Face once (about 770 MB).

**Key concepts:** frozen model, decoder, transposed convolution, reconstruction loss, ceiling and floor, copy-last baseline, shuffled control, train/validation gap.

**Expected computational budget:** Moderate. The frozen model is run once and its outputs are cached; four small decoders are then trained from the cache, a few minutes each.

**Recommended runtime:** **GPU**.

**Estimated student time:** **about 2 hours**, including the picture download.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

## How this example works

This sheet shows what one complete assessment investigation looks like: a question, a prediction, checks before any model is built, controls, and an interpretation. It differs from the weekly practicals in three ways.

- **You investigate before you implement.** The first prompts build nothing. They find out where the pictures, the crops and the vectors are, so that neither you nor Gemini has to guess.
- **You test what Gemini writes.** Each *Check it yourself* box is a short piece of code that **you** write in a new cell, without Gemini. If a check fails, the investigation above it is wrong: go back and fix it before continuing.
- **Gemini answers with a label.** Every chat response must begin with `[BRAINSTORMING]`, `[MAIN]`, `[CLARIFICATION]`, `[CRITICAL]` or `[INTERPRETATION]`. If the label is missing, ask Gemini to reissue the response.

**Before you start.** Run every cell of the reference system. These names must exist: `model`, `img_store`, `clip_store`, `train_ids`, `val_ids`, `StorySequences`, `collate`, `to_device`, `val_loader`. Note the validation `cosine` printed for the last training epoch; you will need it later.

**Write your prediction now.** The baseline predicts a vector for the next frame. If a small network is trained to turn vectors into pictures, how close to the real next frame will the picture made from the *predicted* vector be? As good as the picture made from the real vector? Better than the picture made from the previous frame's vector? Write two sentences and keep them.

---

## Part A — Find out where everything is

## Prompt 1

Copy this into Gemini:

> Ground rules for this whole conversation. Reply in chat only and create no cell for this prompt.
>
> (1) You cannot see the file store.py. Never guess its interface. Use only attributes and functions whose source code or printed output is already visible in this notebook. If you need one you have not seen, say so and ask me to print it.
>
> (2) Never write try/except, hasattr checks, callable checks or silent fallbacks. If a value is None or a shape is unexpected, the code must stop with a clear error.
>
> (3) Do not define or train any new model until I ask for it.
>
> (4) One prompt, one cell. If a cell fails, repair that same cell.
>
> Confirm the rules in three lines.

### Questions

1. Why is a `try/except` that skips a failing frame dangerous inside a training loop? What would the loss look like if every frame were skipped?
2. Gemini can read the cells of your notebook. Why can it still be wrong about how `store.py` behaves?

---

## Prompt 2

> Create one code cell that only prints source code with inspect.getsource. Import FrameView and StoryStore from store and print the source of: StoryStore.__init__, FrameView.image.func, FrameView.crop_windows.fget, FrameView.image_feat_crops.fget and FrameView.image_feat.fget. Print nothing else and write no other code. After I run it, answer in chat, quoting the printed lines: is image a method or an attribute, when is it None, and what decides whether a store has crop windows?

### Questions

1. Is `image` called with brackets or read without them? Which printed line tells you?
2. Which argument of `StoryStore` must change before any picture can be loaded? What is its default?
3. `crop_windows` returns `None` for one of the two image encoders. Which one, and why does that make sense?
4. How is `image_feat` obtained from `image_feat_crops`?

---

## Prompt 3

> Create one code cell that measures, without loading any picture, what the two existing stores contain. For each of img_store and clip_store take frame 0 of story val_ids[0] and print: store.n_crops, store.img_dim, the shape of image_feat_crops, the shape of image_feat, crop_windows, width, height, and whether image is None. Then take one batch from val_loader and print the shapes of batch["img"] and batch["z"]. Print one labelled line per value.

### Questions

1. Which store is the **input** of the baseline model and which one holds its **target**? What are the two vector sizes?
2. How many vectors does one frame have in the CLIP-H store, and which single vector does the model actually predict?
3. What do the four numbers of one crop window mean? What shape is each window?

### Check it yourself A

Write this code yourself in a new cell.

1. Take `f = clip_store[val_ids[0]][0]`. Use `np.allclose` in an `assert` to confirm that `f.image_feat` is the mean of the three rows of `f.image_feat_crops`.
2. Print the length (`np.linalg.norm`) of each of the three crop vectors and of their mean. Are the vectors unit length? Why is the mean shorter than each crop vector?
3. Compute the cosine similarity between the left and the right crop vector of this frame, and between the left crop vectors of two frames from different stories. Which pair is more similar?

---

## Prompt 4

> Re-create clip_store with exactly the same arguments as before plus hf_dataset="auto", so that pictures are fetched from Hugging Face on first use. Then, for frames 0 and 1 of story val_ids[0], show in one figure: the full picture with the three crop windows drawn as rectangles in three colours, and under it the three crops cut out with image.crop. Put the picture size in pixels in the title. Do not resize anything yet.

### Questions

1. Do the three crops overlap? Which part of the frame appears in two crops?
2. The frames have different widths. How do the windows change with the width?
3. The model's target is one vector for the whole frame. From what you see, what does that vector summarise?

---

## Prompt 5

> Write one function frame_crops(frame, size=64). It reads frame.image and frame.crop_windows, cuts the three windows out of the picture, resizes each crop to size x size pixels, and returns one uint8 tensor of shape [3, 3, size, size], meaning [crop, colour channel, height, width]. If frame.image or frame.crop_windows is None it must raise a ValueError with a clear message. Call it once on a frame of clip_store and print the shape, dtype, minimum and maximum. Add a short Markdown explanation of what the function returns and the meaning of each of the four dimensions.

### Questions

1. Why is `uint8` a better storage type than `float32` for many thousands of small pictures?
2. Matplotlib wants `[height, width, channel]`. Which dimensions must be reordered to show one crop?

### Check it yourself B

Write these tests yourself in a new cell.

1. `assert` the shape, the dtype and that all values are between 0 and 255.
2. `assert` that crop 0 and crop 2 are **not** identical (`torch.equal`). Three copies of the same picture would pass a shape test.
3. Show the three crops with `imshow` and compare them with the crops from Prompt 4. Same content, same left-to-right order?
4. Call `frame_crops(img_store[val_ids[0]][0])`. It must raise a `ValueError`. Explain why this store cannot give crops.

---

## Part B — Collect the evidence once

## Prompt 6

> Create one code cell that builds the data for a decoding experiment by running the frozen model exactly once. Call model.eval(), work under torch.no_grad() and create no optimiser.
>
> Set N_TRAIN = 2000 and N_VAL = 300 and mark both with a TRY comment. Write build_cache(ids) and call it on train_ids[:N_TRAIN] and val_ids[:N_VAL] to get train_set and val_set.
>
> Inside build_cache, loop over DataLoader(StorySequences(ids), batch_size=16, shuffle=False, collate_fn=collate) and move each batch with to_device. Compute z_hat = model.image_head(model.encode(img[:, :-1], rows[:, :-1], tokens[:, :-1])) exactly as the evaluate function of the notebook does. For every story b of the batch and every position t that has a real frame t+1 (use frame_mask), append one row: Z_true = z[b, t+1], Z_hat = z_hat[b, t], Z_prev = z[b, t], X = frame_crops(clip_store[story_id][t+1]), story = story_id, frame = t+1.
>
> Return a dict with Z_true, Z_hat and Z_prev as CPU tensors [N, 1024], X as a CPU uint8 tensor [N, 3, 3, 64, 64], and story and frame as lists. Keep X as uint8 and never convert the whole of X to float.
>
> Before normalising, print the mean vector length of Z_true and of Z_hat. Then L2-normalise Z_true, Z_hat and Z_prev.
>
> Finally add Z_shuf: for each row, the Z_true of a random row that belongs to a DIFFERENT story (fixed seed), and a list shuf_story with the story that vector came from.
>
> Print every shape and the time taken. Mark with KEY comments the lines that decide which vector is paired with which picture.

### Questions

1. Every row pairs four different vectors with the **same** picture. Which frame is that picture, and which frame does each vector come from or aim at?
2. `Z_hat[b, t]` is paired with `z[b, t+1]`. Where does this offset of one come from in the model?
3. The printed lengths of `Z_true` and `Z_hat` differ. Which term of the training loss allows that?
4. Why is the model run once here, rather than inside the decoder's training loop?

### Check it yourself C

Write these checks yourself. **Predict the order in check 2 before running it.**

1. Pick a row `i` of `val_set`. Show `val_set["X"][i]` next to `clip_store[story][frame].image` for that row's story and frame. Is it the same picture?
2. Print the mean cosine similarity on `val_set` of `Z_hat` with `Z_true`, of `Z_prev` with `Z_true`, and of `Z_shuf` with `Z_true`. The first number should match the validation `cosine` of the baseline's last epoch. If it does not, the rows are misaligned.
3. `assert` that no row has `story == shuf_story`, and that every Z vector has length 1.
4. `assert` that no story id appears in both `train_set` and `val_set`.

---

## Part C — Decode

## Prompt 7

> Create a Markdown cell and one code cell.
>
> Define ZDecoder: Linear(1024, 16384) and ReLU; reshape the 16384 values to [256, 8, 8]; three ConvTranspose2d layers with kernel 4, stride 2 and padding 1 going 256 -> 128 -> 64 -> 9 channels, with ReLU between them and Sigmoid at the end; reshape the output to [B, 3, 3, 64, 64].
>
> Define val_mse(dec, key): the mean squared error on all of val_set between dec(val_set[key]) and val_set["X"] / 255, computed in batches under torch.no_grad().
>
> Define train_decoder(key, epochs=10, seed=0): call torch.manual_seed(seed), create a new ZDecoder on the device, use Adam with lr 1e-3 and shuffled mini-batches of 64 rows of train_set[key] and train_set["X"], converting each batch of X to float / 255 on the device; loss is MSE. After every epoch record (epoch, train MSE, val_mse). Return the decoder and the history.
>
> Train ONE decoder only: dec_true, hist_true = train_decoder("Z_true"). Plot train and validation MSE against epoch. Set SHOW = [5, 200, 500] and show, for those rows of val_set, the three target crops in the top row and the three reconstructions under them.
>
> In the Markdown, briefly explain what the decoder takes in and gives out, what one transposed convolution does to the spatial size, and why the last layer has 9 channels.

### Questions

1. What survives in the reconstructions (colour, layout, objects, faces, texture) and what does not?
2. Does validation MSE keep falling as long as training MSE does? What does the gap tell you?
3. All three crops come out of one vector. Can the decoder tell the left crop from the right one?

### Check it yourself D

1. Pass `torch.randn(5, 1024)` through a new `ZDecoder()`. `assert` the output shape and that every value lies between 0 and 1.
2. Print the number of parameters of each layer. Predict first: which layer holds most of them, and why?

---

## Prompt 8

**Before running:** write down the order you expect for the four validation errors, best to worst.

> Without changing ZDecoder, val_mse or train_decoder, train three more decoders with the same seed and number of epochs: dec_hat on "Z_hat", dec_prev on "Z_prev" and dec_shuf on "Z_shuf". Also compute a baseline that uses no input at all: the mean training picture (average train_set["X"] in chunks, never converting all of X to float at once) and its MSE on val_set. Print one table with a row per input (Z_true, Z_hat, Z_prev, Z_shuf, constant mean picture) and columns: final train MSE, final val MSE, best val MSE and its epoch. Plot the four validation curves in one figure with the constant baseline as a horizontal line. Show no pictures yet.

### Questions

1. Was your predicted order right? Which result surprised you most?
2. Where does the decoder trained on `Z_shuf` end up, compared with the constant mean picture? What has it learned?
3. Look at the *training* error of the `Z_shuf` decoder over the epochs. Is it learning something? What?
4. Which comparison answers "is the model's prediction better than just repeating the previous frame?" What is the answer in your run?

---

## Prompt 9

> Without training anything, write show_row(i): one figure with 5 rows and 3 columns for row i of val_set. Row 1 the three target crops; row 2 dec_true applied to Z_true[i]; row 3 dec_hat applied to Z_hat[i]; row 4 dec_prev applied to Z_prev[i]; row 5 dec_shuf applied to Z_shuf[i]. Label every row with its name and the MSE of that row against the target, and put the story id and frame index in the figure title. Call show_row for each i in SHOW.

### Questions

1. Does the picture decoded from `Z_hat` look more like the target, like the picture decoded from `Z_prev`, or like neither?
2. Compare the `Z_shuf` row across the three examples. What do you notice?
3. Find one example where the scene changes between frame *t* and frame *t+1* (change `SHOW`). Which rows cope with the change?

---

## Try it yourself manually

Without asking Gemini, go back to the **code cell generated by Prompt 9 in this experiment**. Change one line so that row 3 feeds `Z_hat[i]` into `dec_true`, the decoder that was trained on real vectors, instead of `dec_hat`. Then, in a new cell, print `val_mse(dec_true, "Z_hat")` and `val_mse(dec_true, "Z_prev")`.

Before running, predict: `Z_hat` is the model's best guess of `Z_true` and their cosine similarity is high. Will `dec_true` draw a reasonable picture from it?

- Is `val_mse(dec_true, "Z_hat")` better or worse than the constant mean picture?
- `Z_prev` has a *lower* cosine with `Z_true` than `Z_hat` does. Which of the two does `dec_true` handle better?
- Compute the mean cosine similarity between different rows of `val_set["Z_hat"]`, and the same for `val_set["Z_true"]`. Which set of vectors is more spread out?
- What does this say about using one decoder for both real and predicted vectors?

---

## Reveal: what was this experiment really about?

The pictures were never the point. The decoder is a **measuring instrument**: the error of a decoder trained on some vector tells you how much information about the pixels of frame *t+1* can be read out of that vector. This is the same idea as a probe, and it has the same limit: it shows what is **decodable**, not what the model uses.

An instrument needs a scale, and the four inputs provide it:

- `Z_true` is the **ceiling**: the real vector of the frame being drawn.
- `Z_shuf` and the constant mean picture are the **floor**: no information about this frame.
- `Z_prev` is the **baseline**: the next frame usually resembles the current one.
- `Z_hat` is the **model**. Its number means nothing until it is placed between the others.

Three things usually appear. First, even the ceiling is blurred: one pooled vector does not contain the detail, and mean squared error is minimised by the *average* of all pictures that fit the vector. The loss asked for a blur and got one. Second, a decoder given useless input does not fail randomly. It learns the mean picture, and with more epochs it starts to memorise training pairs. Third, a high cosine similarity between `Z_hat` and `Z_true` does not make them interchangeable. Predicted vectors are themselves averages, crowded into a small region of the space, so a decoder trained only on real vectors has never seen anything like them.

If your `Z_hat` decoder was no better than your `Z_prev` decoder, do not hide it. It is a result about the baseline model, and it agrees with the retrieval numbers the baseline printed next to `copy_last`.

Now ask Gemini:

> Using our table of validation MSE for the decoders trained on Z_true, Z_hat, Z_prev and Z_shuf, the constant mean-picture baseline, the picture grids, the cosine similarities between the Z sets, and the result of feeding Z_hat into dec_true, discuss what evidence we have that the model's predicted vector carries information about the next frame beyond what the previous frame already gives. Separate what the evidence shows from what it does not show. If Z_hat was not clearly better than Z_prev in our run, explain what that could mean instead of forcing a success story, and name one control we have not run.

### Final discussion questions

1. Why are four decoders needed? What could you conclude from the `Z_hat` decoder alone?
2. The decoder shows that information is decodable from a vector. Why is that not proof that the model "imagines" the next frame?
3. Why does MSE produce blurred pictures, and what kind of decoder would you need for sharp ones?
4. The baseline's image loss is cosine distance. Name two properties of `Z_hat` that this loss leaves unconstrained, and say where each one showed up in your results.
5. Go back to the prediction you wrote at the start. What did you get wrong, and which result changed your mind?

---

## From this example to your own investigation

The same steps fit the sections of the assessment notebook.

| Notebook section | In this example |
|---|---|
| 1. Question | Can a picture be decoded from the predicted vector, and is it better than one decoded from the previous frame? |
| 2. Motivation and prediction | The prediction you wrote before Part A. |
| 3. Reference system | The frozen v1 GRU baseline: SigLIP input, CLIP-H target, cosine loss. |
| 4. Proposed experiment | Four decoders that differ only in their input; ceiling, floor and copy-last baseline. |
| 5. Implementation | Prompts 2 to 9 and Checks A to D. |
| 6. Results | The MSE table, the validation curves and the grids. |
| 8. Limitations | A subset of stories, one seed, 64-pixel crops, one decoder architecture, MSE as the only measure. |
| 9. AI interaction record | For example: Prompt 2 (verifying instead of guessing), any check that caught an error, the final discussion. |
| 10. What changed my mind? | Final discussion question 5. |

## When Gemini goes wrong

- **It uses a name you have never seen printed.** Send it back to the output of Prompt 2 and ask which printed line supports the name.
- **A loss is exactly 0, or nothing is displayed.** Something is being skipped. Look for `try/except` or an `if` that silently continues, and ask Gemini to remove it so the real error appears.
- **Training is very slow.** Check that no picture is loaded inside the training loop. Pictures are read once, in Prompt 6.
- **The session runs out of memory.** Something converted all of `X` to float. Keep `X` as `uint8` and convert one batch at a time, or lower `N_TRAIN`.
- **A check fails.** Do not continue. Paste the failing check and its output to Gemini and ask it to repair the cell that built the data.
