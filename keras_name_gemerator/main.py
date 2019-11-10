from keras.models import Model, load_model, save_model
from keras_name_gemerator import dictchars_maker, model_setter, name_generator,\
    name_processor, onehot_vec_maker, sequences_maker, csv_loader
from keras_name_gemerator import trainer

if __name__ == '__main__':
    #trainer.train("models/model.h5", "weights/weights7.h5")
    model = load_model("models/model.h5")
    model.load_weights("weights/weights7.h5")

    datas = csv_loader.load_csv("csv/en_jp_names.csv")
    names = [data[1] for data in datas]
    names, chars = name_processor.process_names(names)

    seqlen = 4
    sequences, lengths, nextchars = sequences_maker.make_sequences(names, seqlen, chars)

    dictchars = dictchars_maker.get_dictchars(names, seqlen)

    for _ in range(20):
        print(name_generator.generate_random_name
              (model, chars=chars, dictchars=dictchars))
