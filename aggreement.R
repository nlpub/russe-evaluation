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

plot(density(df.pairs[, 'mean']))
plot(density(df.pairs[, 'sd']))

alpha <- kripp.alpha(ratings, method='ordinal')
print(alpha)
