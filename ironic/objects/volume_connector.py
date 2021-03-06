#    Copyright (c) 2015 Hitachi, Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_utils import strutils
from oslo_utils import uuidutils
from oslo_versionedobjects import base as object_base

from ironic.common import exception
from ironic.db import api as db_api
from ironic.objects import base
from ironic.objects import fields as object_fields


@base.IronicObjectRegistry.register
class VolumeConnector(base.IronicObject,
                      object_base.VersionedObjectDictCompat):
    # Version 1.0: Initial version
    VERSION = '1.0'

    dbapi = db_api.get_instance()

    fields = {
        'id': object_fields.IntegerField(),
        'uuid': object_fields.UUIDField(nullable=True),
        'node_id': object_fields.IntegerField(nullable=True),
        'type': object_fields.StringField(nullable=True),
        'connector_id': object_fields.StringField(nullable=True),
        'extra': object_fields.FlexibleDictField(nullable=True),
    }

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Convert a list of database entities to a list of formal objects."""
        return [VolumeConnector._from_db_object(cls(context), obj)
                for obj in db_objects]

    # NOTE(xek): We don't want to enable RPC on this call just yet. Remotable
    # methods can be used in the future to replace current explicit RPC calls.
    # Implications of calling new remote procedures should be thought through.
    # @object_base.remotable_classmethod
    @classmethod
    def get(cls, context, ident):
        """Find a volume connector based on its ID or UUID.

        :param context: security context
        :param ident: the database primary key ID *or* the UUID of a volume
                      connector
        :returns: a :class:`VolumeConnector` object
        :raises: InvalidIdentity if ident is neither an integer ID nor a UUID
        :raises: VolumeConnectorNotFound if no volume connector exists with
                 the specified ident
        """
        if strutils.is_int_like(ident):
            return cls.get_by_id(context, ident)
        elif uuidutils.is_uuid_like(ident):
            return cls.get_by_uuid(context, ident)
        else:
            raise exception.InvalidIdentity(identity=ident)

    # NOTE(xek): We don't want to enable RPC on this call just yet. Remotable
    # methods can be used in the future to replace current explicit RPC calls.
    # Implications of calling new remote procedures should be thought through.
    # @object_base.remotable_classmethod
    @classmethod
    def get_by_id(cls, context, db_id):
        """Find a volume connector based on its integer ID.

        :param context: Security context.
        :param db_id: The integer (database primary key) ID of a
                      volume connector.
        :returns: A :class:`VolumeConnector` object.
        :raises: VolumeConnectorNotFound if no volume connector exists with
                 the specified ID.
        """
        db_connector = cls.dbapi.get_volume_connector_by_id(db_id)
        connector = VolumeConnector._from_db_object(cls(context), db_connector)
        return connector

    # NOTE(xek): We don't want to enable RPC on this call just yet. Remotable
    # methods can be used in the future to replace current explicit RPC calls.
    # Implications of calling new remote procedures should be thought through.
    # @object_base.remotable_classmethod
    @classmethod
    def get_by_uuid(cls, context, uuid):
        """Find a volume connector based on its UUID.

        :param context: security context
        :param uuid: the UUID of a volume connector
        :returns: a :class:`VolumeConnector` object
        :raises: VolumeConnectorNotFound if no volume connector exists with
                 the specified UUID
        """
        db_connector = cls.dbapi.get_volume_connector_by_uuid(uuid)
        connector = VolumeConnector._from_db_object(cls(context), db_connector)
        return connector

    # NOTE(xek): We don't want to enable RPC on this call just yet. Remotable
    # methods can be used in the future to replace current explicit RPC calls.
    # Implications of calling new remote procedures should be thought through.
    # @object_base.remotable_classmethod
    @classmethod
    def list(cls, context, limit=None, marker=None,
             sort_key=None, sort_dir=None):
        """Return a list of VolumeConnector objects.

        :param context: security context
        :param limit: maximum number of resources to return in a single result
        :param marker: pagination marker for large data sets
        :param sort_key: column to sort results by
        :param sort_dir: direction to sort. "asc" or "desc".
        :returns: a list of :class:`VolumeConnector` objects
        :raises: InvalidParameterValue if sort_key does not exist
        """
        db_connectors = cls.dbapi.get_volume_connector_list(limit=limit,
                                                            marker=marker,
                                                            sort_key=sort_key,
                                                            sort_dir=sort_dir)
        return VolumeConnector._from_db_object_list(db_connectors,
                                                    cls, context)

    # NOTE(xek): We don't want to enable RPC on this call just yet. Remotable
    # methods can be used in the future to replace current explicit RPC calls.
    # Implications of calling new remote procedures should be thought through.
    # @object_base.remotable_classmethod
    @classmethod
    def list_by_node_id(cls, context, node_id, limit=None, marker=None,
                        sort_key=None, sort_dir=None):
        """Return a list of VolumeConnector objects related to a given node ID.

        :param context: security context
        :param node_id: the integer ID of the node
        :param limit: maximum number of resources to return in a single result
        :param marker: pagination marker for large data sets
        :param sort_key: column to sort results by
        :param sort_dir: direction to sort. "asc" or "desc".
        :returns: a list of :class:`VolumeConnector` objects
        :raises: InvalidParameterValue if sort_key does not exist
        """
        db_connectors = cls.dbapi.get_volume_connectors_by_node_id(
            node_id,
            limit=limit,
            marker=marker,
            sort_key=sort_key,
            sort_dir=sort_dir)
        return VolumeConnector._from_db_object_list(db_connectors,
                                                    cls, context)

    # NOTE(xek): We don't want to enable RPC on this call just yet. Remotable
    # methods can be used in the future to replace current explicit RPC calls.
    # Implications of calling new remote procedures should be thought through.
    # @object_base.remotable
    def create(self, context=None):
        """Create a VolumeConnector record in the DB.

        :param context: security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: VolumeConnector(context).
        :raises: VolumeConnectorTypeAndIdAlreadyExists if a volume
                 connector already exists with the same type and connector_id
        :raises: VolumeConnectorAlreadyExists if a volume connector with the
                 same UUID already exists
        """
        values = self.obj_get_changes()
        db_connector = self.dbapi.create_volume_connector(values)
        self._from_db_object(self, db_connector)

    # NOTE(xek): We don't want to enable RPC on this call just yet. Remotable
    # methods can be used in the future to replace current explicit RPC calls.
    # Implications of calling new remote procedures should be thought through.
    # @object_base.remotable
    def destroy(self, context=None):
        """Delete the VolumeConnector from the DB.

        :param context: security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: VolumeConnector(context).
        :raises: VolumeConnectorNotFound if the volume connector cannot be
                 found
        """
        self.dbapi.destroy_volume_connector(self.uuid)
        self.obj_reset_changes()

    # NOTE(xek): We don't want to enable RPC on this call just yet. Remotable
    # methods can be used in the future to replace current explicit RPC calls.
    # Implications of calling new remote procedures should be thought through.
    # @object_base.remotable
    def save(self, context=None):
        """Save updates to this VolumeConnector.

        Updates will be made column by column based on the result
        of self.obj_get_changes().

        :param context: security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: VolumeConnector(context).
        :raises: VolumeConnectorNotFound if the volume connector cannot be
                 found
        :raises: VolumeConnectorTypeAndIdAlreadyExists if another connector
                 already exists with the same values for type and connector_id
                 fields
        :raises: InvalidParameterValue when the UUID is being changed
        """
        updates = self.obj_get_changes()
        updated_connector = self.dbapi.update_volume_connector(self.uuid,
                                                               updates)
        self._from_db_object(self, updated_connector)

    # NOTE(xek): We don't want to enable RPC on this call just yet. Remotable
    # methods can be used in the future to replace current explicit RPC calls.
    # Implications of calling new remote procedures should be thought through.
    # @object_base.remotable
    def refresh(self, context=None):
        """Load updates for this VolumeConnector.

        Load a volume connector with the same UUID from the database
        and check for updated attributes. If there are any updates,
        they are applied from the loaded volume connector, column by column.

        :param context: security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: VolumeConnector(context).
        """
        current = self.__class__.get_by_uuid(self._context, uuid=self.uuid)
        self.obj_refresh(current)
