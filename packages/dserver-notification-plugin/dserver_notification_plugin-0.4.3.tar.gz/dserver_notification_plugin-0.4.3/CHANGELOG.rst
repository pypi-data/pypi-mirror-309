Change log for dserver-notification-plugin
==========================================

0.4.3 (20Nov24)
---------------

* Detailed logging, more header fields treated.

0.4.2 (20Nov24)
---------------

* Return proper error code on request without content.
* Filter IPs by ``HTTP_X_REAL_IP`` if header entry is present. This is usually the case when header is rewritten by reverse proxy.

0.4.1 (9Jul24)
---------------

* Automated github release creation

0.4.0 (13Jun24)
---------------

* Exchanged ``dtool-lookup-server`` dependency for ``dservercore``

0.3.0 (07Jun24)
---------------

* Rebranded prefix ``dtool-lookup-server-`` to ``dserver-``
* Switched from ``setup.py`` to ``pyproject.toml``
* Adapted to new dserver REST API standard.

0.2.2 (09Mar22)
---------------

* Robust registration of datasets by

0.2.1 (09Mar22)
---------------

* webhook/notify route correctly processes NetApp StorageGRID SNS endpoint S3
  event notifications

0.2.0 (25Feb22)
---------------

* dserver config/info route yields this plugin's config as well
* Introduced webhook/notify route

0.1.1 (23May21)
---------------

* Update for Flask-JWT-Notification >=4.0

0.1.0 (23May21)
---------------

* Listen to elastic-search notifications
* Register and delete datasets based on notification
* IP filtering for security
