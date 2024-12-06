from sklearn.metrics import accuracy_score, mean_squared_error

def test_model(model, X_train, X_test, y_train, y_test, problem_type='classification'):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    if problem_type == 'classification':
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy
    elif problem_type == 'regression':
        mse = mean_squared_error(y_test, y_pred)
        return mse