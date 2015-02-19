# The MIT License (MIT)
#
# Copyright (c) 2014-2015 Dmitry Ustalov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

library(irr)

df <- read.csv('pair_responses.csv', sep=';')
df$pair_id <- factor(df$pair_id)
df$uniqid  <- factor(df$uniqid)
df$score   <- factor(df$score, ordered=T)

df.pairs <- data.frame(pair_id=levels(df$pair_id),
                       count=rep(NA, length(levels(df$pair_id))),
                       mean=rep(NA, length(levels(df$pair_id))),
                       sd=rep(NA, length(levels(df$pair_id))))

ratings <- matrix(nrow=length(levels(df$uniqid)),
                  ncol=length(levels(df$pair_id)))

for (i in 1:nrow(df)) {
  row <- df[i,]
  ratings[row$uniqid, row$pair_id] <- row$score
}

sapply(levels(df$pair_id), function(id) {
  scores <- as.integer(df[df$pair_id == id, 'score']) - 1
  df.pairs[df.pairs$pair_id == id, 'count'] <<- length(scores)
  df.pairs[df.pairs$pair_id == id, 'mean'] <<- mean(scores)
  df.pairs[df.pairs$pair_id == id, 'sd'] <<- sd(scores)
})

plot(density(df.pairs[, 'sd']))
abline(v=mean(df.pairs[, 'sd']))
print(mean(df.pairs[, 'sd']))

alpha <- kripp.alpha(ratings, method='ordinal')
print(alpha)
