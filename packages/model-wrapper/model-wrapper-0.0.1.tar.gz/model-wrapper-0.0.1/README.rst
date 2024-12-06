Usage Sample
''''''''''''

.. code:: python

        from model_wrapper import SplitClassModelWrapper

        classes = ['class1', 'class2', 'class3'...]
        X = [[...], [...],]
        y = [0, 0, 1, 2, 1...]

        model = ...
        model_wrapper = SplitClassModelWrapper(model, classes=classes)
        model_wrapper.train(X, y, val_size=0.2)

        X_test = [[...], [...],]
        y_test = [0, 1, 1, 2, 1...]
        result = model_wrapper.evaluate(X_test, y_test)
        # 0.953125

        result = model_wrapper.predict(X_test)
        # [0, 1]

        result = model_wrapper.predict_classes(X_test)
        # ['class1', 'class2']

        result = model_wrapper.predict_proba(X_test)
        # ([0, 1], array([0.99439645, 0.99190724], dtype=float32))

        result = model_wrapper.predict_classes_proba(X_test)
        # (['class1', 'class2'], array([0.99439645, 0.99190724], dtype=float32))
