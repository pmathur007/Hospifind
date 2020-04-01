import numpy as np
from collections import deque
import tensorflow.keras as keras

class Agent:
    def __init__(self, in_size = 10, out_size = 1, batch_size = 32, epsilon = 1, replay_memory_size = 2000, num_hosp = 10, epochs = 100, cutoff = 10, take = 1):
        self.input_size = in_size
        self.output_size = out_size
        self.anneal_rate = 1 / 2000 #2000, 1500
        self.max_epsilon = epsilon
        self.min_epsilon = 0.0001 #0.001
        self.batch_size = batch_size
        self.memory = deque(maxlen = replay_memory_size)
        self.num_hosp = num_hosp
        self.steps = 0
        self.replay_start_size = batch_size * 2
        self.epochs = epochs
        self.score_cutoff = cutoff
        self.last_take = take

        self.model = keras.Sequential()
        self.model.add(keras.layers.Dense(32,input_shape = (state_size,), activation='tanh'))
        self.model.add(keras.layers.Dense(32, activation = 'tanh'))
        self.model.add(keras.layers.Dense(1, activation = 'tanh'))
        self.model.compile(loss = 'mean_squared_error', optimizer = keras.optimizers.Adam())

        self.train()

    def act(self, patient, hospitals, training=True):
        action = self.policy(patient, hospitals, training)

        if training:
            if self.steps > self.replay_start_size:
                self.train_once()
        else:
            for i in range(len(action)):
                action[i] = round(action[i] * 100.0, 1)
            action.sort(reverse = True)

        return action

    def choose(self, action):
        sum = 0
        for i in action:
            sum+=i
        for i in range(len(action)):
            action[0] = i/sum

        r = np.random.rand()
        x = actions[0]
        index = 0
        while x < r:
            index+=1
            x+=actions[index]
        return index


    def policy(self, patient, hospitals, training):
        self.epsilon = self.max_epsilon - (self.steps * self.anneal_rate)
        self.epsilon = max(self.epsilon,self.min_epsilon)
        explore = self.epsilon > np.random.rand()
        out = []
        if training and explore:
            for i in range(len(hospitals)):
                out.append(np.random.rand())
        else:
            for h in hospitals:
                x = np.asarray(patient.info()+h.info())
                y = self.model.predict(x, verbose = 0)[0]
                out.append(y)
        return out


    def train_once(self):
        index = np.random.choice(
            np.arange(len(self.memory)),
            size = self.batch_size,
            replace = False
        )
        batch = [self.memory[i] for i in index]
        patient = np.array([b["patient"] for b in batch])
        hospital = np.array(b["hospital"] for b in batch)
        output = np.array([b["output"] for b in batch])

        targets = np.squeeze(output)
        inputs = np.squeeze(np.concatenate(np.squeeze(patient), np.squeeze(hospital), axis = None))
        self.model.fit(inputs, targets, verbose = 0, epochs = 2)

    def train(self):
        env = Simulator()
        avg_score = 0

        for e in range(self.epochs):
            done = False
            score = 0
            temp_memory = []
            while not done:
                patient, hospitals = env.new_case()
                action = self.act(patient, hospitals)
                score, done = env.act(self.choose(action))

                for i in range(len(hospitals)):
                    experience = {
                        "patient": patient,
                        "hospital": hospitals[i],
                        "output": actions[i]
                    }
                    temp_memory.append(experience)

            if score > self.score_cutoff:
                for exp in temp_memory[:-1*self.last_take]:
                    self.memory.append(exp)
                    self.steps+=1

            avg_score+=score
            print("episode: {}/{}, score: {}, e: {:.2}"
                  .format(e, self.epochs, score, self.epsilon))

        print("Average Score: ", (avg_score / self.epochs))

    def test(self, patient, hospitals):
        return self.act(patient, hospitals, False)

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
